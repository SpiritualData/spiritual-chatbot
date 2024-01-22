from fastapi import FastAPI
from fastapi.responses import JSONResponse
from spiritualdata_utils import mongo_query_db, mongo_connect_db
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from typing import Dict, List
from loguru import logger

custom_gpt_app = FastAPI()

mongo = mongo_connect_db(uri=os.getenv("MONGO_VECTOR_URI", None), database_name='spiritualdata')

embeddings = OpenAIEmbeddings(chunk_size=1000)
max_top_k = 50
data_sources = ['experiences', 'research', 'hypotheses']

@custom_gpt_app.post("/get_data")
async def get_data(source_queries: Dict[str, List[str]], top_k: int=4):
    # Setting a limit for the top_k value:
    top_k = min(top_k, max_top_k)

    docs = []
    for data_source, queries in source_queries.items():
        if data_source not in data_sources:
            logger.info(f"{data_source} collection not found")
            continue

        for query in queries:
            dense_vec = embeddings.embed_query(query)
            collection = mongo[data_source]

            try:
                results = collection.aggregate(
                    [
                        {
                            "$search": {
                                "index": "default",
                                "knnBeta": {
                                    "vector": dense_vec,
                                    "path": "embedding",
                                    "k": top_k,
                                }
                            }
                        }              
                    ]
                )
                
                for res in results:
                    docs.append({
                        "name": res["name"],
                        "text": res["text"],
                        "url": res["url"],
                    })
            
            except Exception:
                logger.info("Failed to retrieve results")
                return JSONResponse(content={"message": "Failed to retrieve results"}, status_code=404)
        
    return JSONResponse(content=docs)