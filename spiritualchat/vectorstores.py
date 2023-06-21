# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  
)
index_name = "mlqai"

docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)