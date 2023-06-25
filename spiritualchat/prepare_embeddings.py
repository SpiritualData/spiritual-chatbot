from langchain.text_splitter import RecursiveCharacterTextSplitter
from spiritualchat.vectorstores import index_name
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import os

def prepare_embeddings(filepath, dataset: str, chunk_size=1000, chunk_overlap=100, column_to_embed='Description'):
    """
    Args:
        - filepath (str): Filepath containing Notion export of documents with 'description' column.
        - dataset (str): Data to be embedded. This is used for namespace. One of 'experiences', 'research', 'hypotheses'
        - chunk_size (int): Size of each chunk (default: 1000).
        - chunk_overlap (int): Overlap between consecutive chunks (default: 20).

    Returns:
        list: List of split documents.
    Implementation:
        1. Use the Notion API to get 'Description' field from each row in Spiritual Research (https://www.notion.so/spiritualdata/15b002ffae8e4ccdad4b55a8f619eea8?v=b32c8d520e144c568f1ac60af1cadac4) and Spiritual Experiences (https://www.notion.so/spiritualdata/6c8b84da23054462a3d8bdaa2e1c4968?v=9df4e3c4950744059ba1527d98e85bee).
        2. Embed description using OpenAI ada 002 embedding with langchain.
    """
    loader = CSVLoader(file_path=filepath, encoding="utf-8", csv_args={'delimiter': ','}, source_column='Description')
    documents = loader.load()
    for doc in documents:
        print(doc)
        break
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    texts = text_splitter.split_documents(documents)
    for text in texts:
        print(type(text), text)
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

    index = pinecone.Index(index_name)

    # Add embeddings to Pinecone with metadata and namespace
    index.upsert(
        # TODO
        namespace=dataset
        )
    # index = Pinecone.from_documents(texts, embeddings, index_name=index_name)
    return texts

##################### Archive
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader

def document_loader(file_path, encoding="utf-8", csv_args={'delimiter': ','}):
    """
    Args:
        file_path (str): Path to CSV file.
        encoding (str): Encoding of CSV file (default: utf-8).
        csv_args (dict): Arguments to be passed to csv.reader (default: {'delimiter': ','}).

    Returns:
        - documents (list of str): Each document is a row from the CSV file.
    """
    loader = CSVLoader(file_path=file_path, encoding=encoding, csv_args=csv_args)
    documents = loader.load()
    return documents

