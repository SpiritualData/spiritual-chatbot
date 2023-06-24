from langchain.vectorstores import Pinecone
import os
embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
# initialize pinecone
pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'),  # find at app.pinecone.io
    environment=os.environ.get('PINECONE_API_ENV')
)
index_name = "experiences-index"

def load_existing_embeddings(index_name):
    """
    Args:
        index_name (str): Name of Pinecone index.
    Returns:
        - index (Pinecone): Pinecone index.
    """
    index = Pinecone.from_existing_index(index_name, embeddings)
    return index