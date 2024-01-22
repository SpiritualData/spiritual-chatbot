from fastapi import FastAPI, HTTPException
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
supported_data_sources = ['experiences', 'research', 'hypotheses']

@custom_gpt_app.post("/get_data")
async def get_data(source_queries: Dict[str, List[str]], top_k: int = 4):
    # Setting a limit for the top_k value:
    top_k = min(top_k, max_top_k)

    # Initializing the response structure:
    response_data = {data_source: {} for data_source in supported_data_sources if data_source in source_queries}

    for data_source, queries in source_queries.items():
        if data_source not in supported_data_sources:
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

                query_results = []
                for res in results:
                    query_results.append({
                        "name": res["name"],
                        "text": res["text"],
                        "url": res["url"],
                    })

                # Adding results to the corresponding query and data source
                if query_results:
                    if query not in response_data[data_source]:
                        response_data[data_source][query] = query_results
                    else:
                        response_data[data_source][query].extend(query_results)
            
            except Exception as e:
                logger.error(f"Failed to retrieve results for {data_source} due to {e}")
                continue  # Using continue to try next queries instead of stopping the loop

    if not any(response_data.values()):  # Checking if the response_data is empty
        raise HTTPException(status_code=404, detail="No results found")

    return JSONResponse(content=response_data)
