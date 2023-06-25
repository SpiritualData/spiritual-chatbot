import pinecone
import os

# initialize pinecone
pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'),  # find at app.pinecone.io
    environment=os.environ.get('PINECONE_API_ENV')
)

index_name = os.environ.get('PINECONE_INDEX_NAME', 'prototype')
namespaces = ['experiences', 'research', 'hypotheses']

def load_existing_embeddings(index_name, data_type):
    """
    Args:
        - index_name (str): Name of Pinecone index.
        - data_type (str): Data to be embedded. One of 'experiences', 'research', 'hypotheses'.

    Returns:
        - index (Pinecone): Pinecone index.
    """
    index = pinecone.Pinecone.from_existing_index(vector_indices[data_type], embeddings)
    return index