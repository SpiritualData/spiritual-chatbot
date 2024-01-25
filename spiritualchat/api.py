"""
Uses query_chatbot to send chatbot response back to user. When the chatbot is done

/chat/response
Request:
{
    "chat_id": "123456",
    "message": "What experiences talk about users?"
}
Response:
{
    "ai": "...",

    "db_results": {
        "hypotheses": [
            {
                "url": "https://www.example.com/hypothesis1",
                "name": "...",
                "snippet": "..."
            }
        ],
        "experiences": [
            {
                "url": "https://www.example.com/experience1",
                "name": "...",
                "snippet": "..."
            }
        ],
        "research": [
            {
                "url": "https://www.example.com/research1",
                "name": "...",
                "snippet": "..."
            }
        ]
    }
}

/chat/title
Request:
    { message: "" }
Response:
    { chat_id:"", title: "" }
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from spiritualchat import query_chatbot
from spiritualchat import get_chat_history_manager
from jose import jwt, JWTError
import json
import httpx
from typing import Dict, Any, Optional, List, Union
from loguru import logger
from cachetools import cached, TTLCache
import os
import datetime
from spiritualdata_utils import init_logger

init_logger()

app = FastAPI()

security = HTTPBearer()

# CORS configuration
origins_str = os.environ.get("ORIGINS")
origins = origins_str.split(",")
origins_set = set(origins)
logger.info("origins: " + str(origins))

clerk_public_key = os.environ.get("CLERK_PEM_PUBLIC_KEY")
clerk_api_key = os.environ.get("CLERK_API_KEY")
logger.info("clerk_api_key: " + str(clerk_api_key))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The TTLCache will hold up to 100,000 items, each of which will live for 7 days.
# After 7 days, if an item is not accessed, it will be evicted from the cache.
token_cache = TTLCache(maxsize=100000, ttl=7 * 24 * 60 * 60)

CLERK_API_URL = "https://api.clerk.dev/v1"


async def decode_jwt(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    logger.info("token: " + str(token))

    # Check cache for session id
    session_tuple = token_cache.get(token)
    logger.info(f"session_tuple: {session_tuple}")
    if session_tuple is None:
        # Extract session id from the token without verification
        try:
            decoded_token = jwt.decode(
                token, None, options={"verify_signature": False, "verify_exp": False}
            )
            logger.info(f"decoded_token: {decoded_token}")
        except jwt.ExpiredSignatureError as e:
            logger.error(e)
            raise HTTPException(status_code=401, detail=f"Token has expired: {str(e)}")
        except jwt.JWTClaimsError as e:
            logger.error(e)
            raise HTTPException(
                status_code=401,
                detail=f"Invalid claims. Please check the audience and issuer: {str(e)}",
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=401,
                detail=f"Unable to parse authentication token: {str(e)}",
            )
        session_id = decoded_token.get("sid")

        if not session_id:
            raise HTTPException(
                status_code=401, detail="Invalid token. Unable to extract session id."
            )

        logger.info(f"Got session {session_id}")

        # Clerk's API endpoint for checking a session's status.
        api_url = f"{CLERK_API_URL}/sessions/{session_id}/verify"

        # Make a request to Clerk's API.
        headers = {
            "Authorization": f"Bearer {os.getenv('CLERK_API_KEY')}",
            "Content-Type": "application/json",
        }
        payload = {"token": token}
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, headers=headers, json=payload)
        logger.info(f"Clerk response: {response}")
        # Check if the session is active.
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token.")

        # If the session is active, we trust the user's identity.
        user_id = decoded_token.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401, detail="Invalid token. Unable to extract user id."
            )

        # Add session id to cache
        token_cache[token] = (session_id, user_id)
        logger.info(f"Remembering session {session_id}")
    else:
        session_id, user_id = session_tuple
    return user_id


class ChatRequest(BaseModel):
    chat_id: str
    message: str
    return_results: Optional[bool]
    data_sources: Optional[List[str]]
    answer_model: Optional[str]
    save: Optional[bool]


class ChatResponse(BaseModel):
    ai: str
    db_results: Optional[dict]
    title: Optional[str]
    chat_id: Optional[str]


@app.post("/chat/response", response_model=ChatResponse)
async def respond(
    request: ChatRequest, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = await decode_jwt(credentials)
    chat_id = request.chat_id
    logger.info("chat_id:", chat_id)
    chat_history, chat_id = get_chat_history_manager().get_chat_history(
        user_id, chat_id
    )
    message = request.message
    logger.info("message:", message)
    kwargs = {}
    if request.data_sources is not None:
        kwargs["data_sources"] = request.data_sources
    if request.return_results is not None:
        kwargs["return_results"] = request.return_results
    if request.answer_model is not None:
        kwargs["answer_model"] = request.answer_model
    if request.save is not None:
        kwargs["save"] = request.save
    response = query_chatbot(message, chat_history, **kwargs)
    api_response = ChatResponse(**response)
    api_response.chat_id = chat_id

    return api_response


class ChatHistoryResponse(BaseModel):
    chat_id: str
    title: str


@app.get(
    "/chat/list",
    response_model=List[ChatHistoryResponse],
    dependencies=[Depends(security)],
)
async def get_chat_list(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = await decode_jwt(credentials)

    chats = get_chat_history_manager().get_user_chats(user_id)
    response = [
        ChatHistoryResponse(chat_id=chat_id, title=chat.get("title") or "Chat Title")
        for chat_id, chat in chats.items()
    ]

    return response


class ChatDataResponse(BaseModel):
    chat_id: str
    chat: List[dict]


@app.get("/chat/get", response_model=ChatDataResponse)
async def get_chat(
    chat_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = await decode_jwt(credentials)

    chat, chat_id = get_chat_history_manager().get_chat_history(user_id, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_data = [
        {
            "role": "ai" if "ai" in type(message).__name__.lower() else "user",
            "content": message.content,
        }
        for message in chat.messages
    ]
    response = ChatDataResponse(chat_id=chat_id, chat=chat_data)

    return response


class DeleteChatResponse(BaseModel):
    success: bool


@app.delete("/chat/delete", response_model=DeleteChatResponse)
async def delete_chat(
    chat_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = await decode_jwt(credentials)

    success = get_chat_history_manager().delete_chat(user_id, chat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")

    return DeleteChatResponse(success=success)


"""
Custom GPT / Data API
"""
from fastapi import FastAPI, HTTPException
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from spiritualdata_utils import mongo_query_db, mongo_connect_db
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from typing import Dict, List
from loguru import logger

mongo = mongo_connect_db(uri=os.getenv("MONGO_VECTOR_URI", None), database_name='spiritualdata')

embeddings = OpenAIEmbeddings(chunk_size=1000)
max_top_k = 50
supported_data_sources = ['experiences', 'research', 'hypotheses']

@app.post("/get_data")
async def get_data(source_queries: Dict[str, List[str]], api_key: str, top_k: int = 4):
    expected_api_key = os.environ.get('CUSTOM_GPT_API_KEY')

    if expected_api_key != api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")

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

