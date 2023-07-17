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
from spiritualchat.api_functions.query_chatbot import query_chatbot
from spiritualchat.api_functions.chat_history import get_chat_history_manager
from jose import jwt, JWTError
from jose.utils import base64url_decode
import httpx
import json
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
origins_str = os.environ.get('ORIGINS')
origins = origins_str.split(',')
origins_set = set(origins)
logger.info('origins: '+str(origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JWKS:
    def __init__(self):
        self.jwks = None
        self.expiration = None

    async def get(self):
        now = datetime.datetime.now()
        if self.jwks is None or self.expiration < now:
            async with httpx.AsyncClient() as client:
                clerk_url = os.getenv('CLERK_URL', 'https://api.clerk.dev')  # use a default value in case the environment variable is not set
                res = await client.get(f'{clerk_url}/v1/jwks')
                res.raise_for_status()  # This will raise an HTTPError if the response had an HTTP error status.
                self.jwks = res.json()
                self.expiration = now + datetime.timedelta(hours=1)  # expire after one hour
        return self.jwks

jwks = JWKS()

# JWT Verification and decoding
async def decode_jwt(credentials):
    """
    Decode token and check that it was from one of our origins.
    """
    try:
        jwt = await jwks.get()  # Use the new get_jwks function
        token = credentials.credentials.replace("Bearer ", "")
        header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwt["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    options={"verify_exp": True}
                )
                
                # Checking 'azp' claim against the origins
                if 'azp' in payload:
                    if payload['azp'] not in origins_set:
                        raise HTTPException(
                            status_code=401,
                            detail="Invalid token",
                        )

                user_id = payload.get('sub')
                if user_id is None:
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid token",
                    )
                return user_id
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden",
        )
    raise HTTPException(
        status_code=403,
        detail="Access forbidden",
    )

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

# FastAPI endpoint
@app.post("/chat/response", dependencies=[Depends(security)])
async def chat(request: ChatRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = await decode_jwt(credentials)

    chat_id = request.chat_id
    chat_history, chat_id = get_chat_history_manager().get_chat_history(user_id, chat_id)
    message = request.message
    kwargs = {}
    if request.data_sources is not None:
        kwargs['data_sources'] = request.data_sources
    if request.return_results is not None:
        kwargs['return_results'] = request.return_results
    if request.answer_model is not None:
        kwargs['answer_model'] = request.answer_model
    if request.save is not None:
        kwargs['save'] = request.save
    response = query_chatbot(message, chat_history, **kwargs)
    api_response = ChatResponse(**response)
    api_response.chat_id = chat_id

    return api_response


class ChatHistoryResponse(BaseModel):
    chat_id: str
    title: str

@app.get("/chat/list", response_model=List[ChatHistoryResponse], dependencies=[Depends(security)])
async def get_chat_history(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = await decode_jwt(credentials)

    chats = get_chat_history_manager().get_user_chats(user_id)
    response = [ChatHistoryResponse(chat_id=chat_id, title=chat.get('title') or "Chat Title") for chat_id, chat in chats.items()]
    
    return response


class ChatDataResponse(BaseModel):
    chat_id: str
    chat: List[dict]

@app.get("/chat/get", response_model=ChatDataResponse, dependencies=[Depends(security)])
async def get_chat(chat_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = await decode_jwt(credentials)

    chat, chat_id = get_chat_history_manager().get_chat_history(user_id, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_data = [{"role": type(message).__name__.lower(), "content": message.content} for message in chat.messages]
    response = ChatDataResponse(chat_id=chat_id, chat=chat_data)
    
    return response


class DeleteChatResponse(BaseModel):
    success: bool

@app.delete("/chat/delete", response_model=DeleteChatResponse, dependencies=[Depends(security)])
async def delete_chat(chat_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = await decode_jwt(credentials)

    success = get_chat_history_manager().delete_chat(user_id, chat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")

    return DeleteChatResponse(success=success)
