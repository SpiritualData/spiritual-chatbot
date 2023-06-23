"""
Uses LangChain, Pinecone, and GPT-4 for a chatbot that interacts with vectorstores for spiritual information.

Implementation details:
- Provide the user input to the chat bot and use GPT-4 via langchain to extract text to embed for each vector store, where relevant.
- Given the answers from the chatbot about the input, query for related data from our database and ask the chat bot to explain this data to the user in a particular way.

"""
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from spiritualchat.vectorstores import pinecone
from collections import defaultdict

chat_history = defaultdict(lambda: defaultdict(list))
def get_chat_history(user_id: str, chat_id: str):
	global chat_history
	if not chat_id:
		chat_id = 0
	return chat_history[user_id][chat_id], chat_id

def append_chat_history(user_id: str, chat_id: str, messages: list):
	global chat_history
	chat_history[user_id][chat_id].extend(messages)

chain = None
def query_chatbot(user_input: str):
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
	"""
	global chain
	# if chain is None:
	# 	chain = create_chat_chain()
	# chain.run(input_documents=docs, question=query)
	return {'ai': "Hello world. I'm a Spiritual Data chatbot.", 'db_results': {'experiences': [{'url': 'https://spiritualdata.org', 'snippet': 'This happened.', 'name': 'My experience'}]}}

def create_chat_chain():
	llm = OpenAI(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'])
	chain = load_qa_chain(llm, chain_type="stuff")

	extract_query_texts(user_input)

	docs = docsearch.similarity_search(query, include_metadata=True)
	docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
	prompt = """Given this input from the user, provide the following JSON format without anything else in your response:
	{"hypotheses_queries": ["<Text to embed>"],
	"research_queries": ["<Text to embed>"],
	"experiences_queries": ["<Text to embed>"]}
	There may be more than one query per type. Ensure the text to embed is a string that represents what the user is asking in relation to the particular type of documents the query is for.
	"""

def extract_query_texts(text, information_types=['experiences', 'research', 'hypotheses']):
	"""
	Get texts to embed, by information_types.
	"""
	return
