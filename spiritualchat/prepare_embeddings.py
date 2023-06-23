from langchain.text_splitter import RecursiveCharacterTextSplitter
from spiritualchat.vectorstores import pinecone


def prepare_embeddings():
    """
    Args:
        -

    Implementation:
        1. Use the Notion API to get 'Description' field from each row in Spiritual Research (https://www.notion.so/spiritualdata/15b002ffae8e4ccdad4b55a8f619eea8?v=b32c8d520e144c568f1ac60af1cadac4) and Spiritual Experiences (https://www.notion.so/spiritualdata/6c8b84da23054462a3d8bdaa2e1c4968?v=9df4e3c4950744059ba1527d98e85bee).
        2. Embed description using OpenAI ada 002 embedding with langchain.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    texts = text_splitter.split_documents(documents)
    return docs

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

def split_document(text, max_chars=1000):
    """
    Returns:
        - segments (list of str): Each segment is witin max_chars, while not separating sentences.
    """
    # TODO
    return segments

