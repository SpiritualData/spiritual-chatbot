from spiritualchat import query_chatbot
import pytest
import requests
from pydantic import BaseModel

class ChatRequest(BaseModel):
    chat_id: str
    message: str

class ChatResponse(BaseModel):
    ai: str
    db_results: dict
    title: str

def test_chat_endpoint():
    # Prepare the request
    request = ChatRequest(chat_id='test_chat_id', message='How are you?')

    # Send the request to the endpoint
    response = requests.post('http://localhost:8000/chat/response', json=request.dict())

    # Assert that the status code is 200 (successful)
    assert response.status_code == 200

    # Parse the response
    api_response = ChatResponse(**response.json())

    # Check that the response has the expected properties
    assert api_response.ai is not None and api_response.ai and isinstance(api_response.ai, str)
    assert api_response.db_results is not None
    assert isinstance(api_response.title, str) and api_response.title

    # Add more assertions as needed, based on your requirements
