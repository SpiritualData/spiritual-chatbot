import pinecone
import os
from weaviate import Client, AuthApiKey

# initialize pinecone
# pinecone.init(
#     api_key=os.environ.get('PINECONE_API_KEY'),  # find at app.pinecone.io
#     environment=os.environ.get('PINECONE_API_ENV')
# )

# initialize weaviate
# auth_config = AuthApiKey(api_key=os.environ.get('WEAVIATE_API_KEY'))
# url = os.environ.get('WEAVIATE_URL')

# vector_client = Client(
#   url=url,
#   auth_client_secret=auth_config
# )

# metadata_fields = ["experience_type", "situation_tags", "content_tags", "after_effects_tags", "data_experience", 
#                    "age", "date_reported", "gender", "date_published", "authors", "date_published", "topic_tags", "chunk_index"]

'''
# DEFINING VECTOR DATABASE SCHEMA (FOR WEAVIATE)
experience_schema = {
    "class": "experiences",
    "description": "A collection of spiritual data",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
          "model": "ada",
          "modelVersion": "002",
          "type": "text",
        }
      },
    "properties": [
        {
            "name": "vectordb_id",
            "dataType": [ "text" ],
            "description": "Unique identifier for each entry",
            "moduleConfig": { "text2vec-openai": {"skip": True} },
        },
        {
            "name": "metadata",
            "dataType": [ "object" ],
            "description": "Metadata for each entry",
            "nestedProperties": [
              {"dataType": ["text[]"], "name": 'experience_type'},
              {"dataType": ["text[]"], "name": 'situation_tags'},
              {"dataType": ["text[]"], "name": 'content_tags'},
              {"dataType": ["text[]"], "name": 'after_effects_tags'},
              {"dataType": ["text"], "name": 'data_experience'},
              {"dataType": ["text"], "name": 'age'},
              {"dataType": ["text"], "name": 'date_reported'},
              {"dataType": ["text"], "name": 'gender'},
              {"dataType": ["int"], "name": "chunk_index"},
            ],
            "moduleConfig": { "text2vec-openai": {"skip": True} },
        },
    ],
}

research_schema = {
    "class": "research",
    "description": "A collection of spiritual data",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
          "model": "ada",
          "modelVersion": "002",
          "type": "text",
        }
      },
    "properties": [
        {
            "name": "vectordb_id",
            "dataType": [ "text" ],
            "description": "Unique identifier for each entry",
            "moduleConfig": { "text2vec-openai": {"skip": True} },
        },
        {
            "name": "metadata",
            "dataType": [ "object" ],
            "description": "Metadata for each entry",
            "nestedProperties": [
              {"dataType": ["text[]"], "name": 'authors'},
              {"dataType": ["text"], "name": 'date_published'},
              {"dataType": ["text[]"], "name": 'topic_tags'},
              {"dataType": ["int"], "name": "chunk_index"},
            ],
            "moduleConfig": { "text2vec-openai": {"skip": True} },
        },
    ],
}

# CREATING THE CLASS (NOT NEEDED ANYMORE, A ONE-TIME DEAL)
client.schema.create_class(experience_schema)
client.schema.create_class(research_schema)

# TO DELETE THE CLASS IF NEEDED
if client.schema.exists("SpiritualData"):
  client.schema.delete_class("SpiritualData")

# CONFIGURE BATCH IMPORTS
client.batch.configure(
    batch_size=100,
    dynamic=True,
    timeout_retries=3,
)

# APPLYING PRODUCT QUANTIZATION COMPRESSION (NOT NEEDED ANYMORE, A ONE-TIME DEAL)
client.schema.update_config("SpiritualData", {
  "vectorIndexConfig": {
    "pq": {
      "enabled": True,
      "trainingLimit": 100000,
      "segments": 96  # Options for text-emedding-ada-002 model are 512, 384, 256, 192, 96 (A larger segments parameter means higher memory usage and recall)
    }
  }
})
'''

# index_name = os.environ.get('PINECONE_INDEX_NAME', 'prototype')
# vector_index = pinecone.Index(index_name)
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