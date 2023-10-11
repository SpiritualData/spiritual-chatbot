"""
Uses LangChain, Pinecone, and GPT-4 for a chatbot that interacts with vectorstores for spiritual information.

Implementation details:
- Provide the user input to the chat bot and use GPT-4 via langchain to extract text to embed for each vector store, where relevant.
- Given the answers from the chatbot about the input, query for related data from our database and ask the chat bot to explain this data to the user in a particular way.

"""
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferWindowMemory
from spiritualchat.vectorstores import vector_index
from spiritualchat.api_functions.pinecone_namespacesearch import PineconeNamespaceSearchRetriever, NamespaceSearchConversationalRetrievalChain
from spiritualchat.api_functions.prompts import create_condense_prompt, create_qa_prompt
from spiritualchat.api_functions.chat_history import chat_history_to_str
from langchain.embeddings.openai import OpenAIEmbeddings
from loguru import logger


chain = None
embeddings = OpenAIEmbeddings(chunk_size=1000)
def query_chatbot(user_input: str, chat_history, namespaces=['experiences', 'research', 'hypotheses'], title=None, memory_k=2, parsing_model='gpt-3.5-turbo', answer_model='gpt-3.5-turbo', max_tokens_limit=4000, return_results=True, save=True, timeout_seconds=180, **kwargs):
    """
    Returns:
        {
        "ai_response": "",

        "db_results": {
            "hypotheses": [
                {
                    "url": str,
                    "name": str,
                    "snippets": [str]
                }
            ],
            "experiences": [
                {
                    "url": str,
                    "name": str,
                    "snippets": [str]
                }
            ],
            "research": [
                {
                    "url": str,
                    "name": str,
                    "snippets": [str]
                }
            ]
        }
    }

    Implementation details:
        1. Use LangChain's ConversationalRetrievalChain with a custom condense_question_prompt to get embedding texts per document type (or Pinecone index namespace).
        2. Implement a custom BaseRetriever that makes Namespaceple Pinecone queries given a list of queries by namespace from user input (using condense_question_prompt)
    """
    global chain
    global embeddings
    logger.info('kwargs:', kwargs)
    chat_history_str = chat_history_to_str(chat_history, max_messages=memory_k)
    kwargs['prompt'] = create_qa_prompt(chat_history_str)
    output_key = "answer"
    if chain is None:
        chain = NamespaceSearchConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0,model_name=parsing_model,request_timeout=timeout_seconds),
            retriever=PineconeNamespaceSearchRetriever(embeddings=embeddings, index=vector_index),
            condense_question_prompt=create_condense_prompt(generate_title=title is None, namespaces=namespaces, chat_history_str=chat_history_str),
            condense_question_llm=ChatOpenAI(temperature=0,model_name=answer_model,request_timeout=timeout_seconds),
            output_key=output_key,
            # We only keep the last k interactions in memory
            memory=ConversationBufferWindowMemory(k=memory_k,
                memory_key="chat_history",
                input_key="question", 
                output_key=output_key, 
                ai_prefix='Chatbot', 
                human_prefix='User',
                chat_memory=chat_history),
            max_tokens_limit=max_tokens_limit,
            combine_docs_chain_kwargs=kwargs,
            verbose=False
        )
    result = chain(inputs=dict(question=user_input, chat_history=chat_history, chat_history_str=chat_history_str))
    response = {'ai': result['answer']}
    if return_results:
        db_results = {}
        for namespace, sources in result['source_documents'].items():
            formatted_sources = []
            for source in sources:
                split_id = source.metadata['id'].rsplit('_', 1)
                url = split_id[0] if len(split_id) > 1 else source.metadata['id']
                url = url.replace('experiences/', 'Experiences/')
                split_content = source.page_content.split('\n', 1)
                name = split_content[0] if len(split_content) > 0 else 'Unnamed document'
                snippet = split_content[1] if len(split_content) > 1 else 'Document content missing'
                formatted_sources.append({
                    'url': url,
                    'snippet': snippet,
                    'name': name
                })
            db_results[namespace] = formatted_sources
        response['db_results'] = db_results
    if 'title' in result:
        title = result['title']
        response['title'] = title
    else:
        # Don't need to store title since it was already stored in an earlier call
        title = None
    if save:
        chat_history.save_chat(title=title)
    return response
