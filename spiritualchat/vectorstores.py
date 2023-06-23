import pinecone
import os

# initialize pinecone
pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'),  # find at app.pinecone.io
    environment=os.environ.get('PINECONE_API_ENV')
)
index_name = "experiences-index"

# docsearch = pinecone.Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)