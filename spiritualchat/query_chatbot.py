"""
Uses LangChain, Pinecone, and GPT-4 for a chatbot that interacts with vectorstores for spiritual information.

Implementation details:
- Provide the user input to the chat bot and use GPT-4 via langchain to extract text to embed for each vector store, where relevant.
- Given the answers from the chatbot about the input, query for related data from our database and ask the chat bot to explain this data to the user in a particular way.

"""
from langchain.llms import OpenAIChat
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from spiritualchat.vectorstores import pinecone
from spiritualchat.pinecone_multisearch import PineconeMultiSearchRetriever
from spiritualchat.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT, SYSTEM_PROMPT
from collections import defaultdict

chat_history = defaultdict(lambda: defaultdict(list))
last_chat_id = 0
def get_chat_history(user_id: str, chat_id: str):
    global chat_history
    global last_chat_id
    if not chat_id:
        chat_id = last_chat_id + 1
        last_chat_id = chat_id
    return chat_history[user_id][chat_id], chat_id

def append_chat_history(user_id: str, chat_id: str, messages: list):
    global chat_history
    chat_history[user_id][chat_id].extend(messages)

chain = None
def query_chatbot(user_input: str, datasets=['experiences', 'research', 'hypotheses'], memory_k=2, parsing_model='gpt3.5-turbo', answer_model='gpt3.5-turbo', **kwargs):
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
        2. Implement a custom BaseRetriever that makes multiple Pinecone queries given a list of queries by namespace from user input (using condense_question_prompt)
    """
    global chain
    if chain is None:
        chain = ConversationalRetrievalChain.from_llm(
            llm=OpenAIChat(temperature=0,model_name=parsing_model),
            retriever=PineconeMultiSearchRetriever(),
            condense_question_prompt=CONDENSE_QUESTION_PROMPT,
            condense_question_llm=OpenAIChat(temperature=0,model_name=answer_model),
            # We only keep the last k interactions in memory
            memory=ConversationBufferWindowMemory(k=memory_k),
            combine_docs_chain_kwargs=kwargs,
            verbose=True
        )
    chain.run(question=user_input)
    return {'ai': "Hello world. I'm a Spiritual Data chatbot.", 'db_results': {'experiences': [{'url': 'https://spiritualdata.org', 'snippet': 'This happened.', 'name': 'My experience'}]}}
