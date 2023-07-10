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
from spiritualchat import query_chatbot, get_chat_history
from jose import jwt, JWTError
from jose.utils import base64url_decode
import httpx
import json
from typing import Dict, Any, Optional, List
from loguru import logger

from spiritualdata_utils import init_logger

init_logger()

app = FastAPI()

security = HTTPBearer()

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://18.189.128.76:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    chat_id: str
    message: str
    return_results: Optional[bool]
    data_sources: Optional[List[str]]
    answer_model: Optional[str]

class ChatResponse(BaseModel):
    ai: str
    db_results: Optional[dict]
    title: Optional[str]
    chat_id: Optional[str]

# Fetch the JWT Key Set (JWKS) from the Clerk API
async def get_jwks() -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get('https://api.clerk.dev/v1/jwks')
            res.raise_for_status()  # This will raise an HTTPError if the response had an HTTP error status.
            return res.json()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or expired token")

# JWT Verification and decoding
async def decode_jwt(token: str, jwks: dict):
    header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                options={"verify_exp": True}
            )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=403,
                detail="Access forbidden",
            )
    raise HTTPException(
        status_code=403,
        detail="Access forbidden",
    )

# FastAPI endpoint
@app.post("/chat/response", dependencies=[Depends(security)])
async def chat(request: ChatRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    # jwks = await get_jwks()
    # auth_token = credentials.credentials
    # payload = await decode_jwt(auth_token, jwks)
    # if auth_token:
    #     auth_token = auth_token.replace("Bearer ", "")
    #     payload = await decode_jwt(auth_token, jwks)
    #     user_id = payload['sub']  # Get the user id from JWT payload
    # else:
    #     user_id = 0  # Or handle it differently, for example by raising an error
    user_id = 0
    chat_id = request.chat_id
    logger.info(request.return_results)
    chat_history, chat_id = get_chat_history(user_id, chat_id)
    message = request.message
    kwargs = {}
    if request.data_sources is not None:
        kwargs['data_sources'] = request.data_sources
    if request.return_results is not None:
        kwargs['return_results'] = request.return_results
    if request.answer_model is not None:
        kwargs['answer_model'] = request.answer_model
    response = query_chatbot(message, chat_history, **kwargs)
    api_response = ChatResponse(**response)
    api_response.chat_id = chat_id

    return api_response