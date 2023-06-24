from langchain.vectorstores import Pinecone
import os

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
# initialize pinecone
pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'),  # find at app.pinecone.io
    environment=os.environ.get('PINECONE_API_ENV')
)
index_name = "experiences-index"

def create_embeddings(texts):
    """
    Args:
        texts (list): List of texts to be embedded.

    Returns:
        - embeddings (list of np.array): List of embeddings.
    """
    index = Pinecone.from_documents(texts, embeddings, index_name=index_name)
    return index


