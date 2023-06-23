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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from spiritualchat import query_chatbot, get_chat_history, append_chat_history

app = FastAPI()

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

class ChatResponse(BaseModel):
    ai: str
    db_results: dict
    title: str
    chat_id: str

@app.post('/chat/response', response_model=ChatResponse)
def chat(request: ChatRequest):
    chat_id = request.chat_id
    user_id = 0
    chat_history, chat_id = get_chat_history(user_id, chat_id)
    message = request.message

    chat_history.append({'type': 'human', 'message': message})
    response = query_chatbot(chat_history)
[[]]
    chat_history.append({'type': 'ai', 'message': response['ai']})
    append_chat_history(user_id, chat_id, chat_history)

    api_response = ChatResponse(ai=response['ai'], db_results=response['db_results'], title="Spiritual Chat", chat_id=chat_id)
    return api_response
