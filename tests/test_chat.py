import pytest
from fastapi.testclient import TestClient
from main import app
from services import ai_service

client = TestClient(app)

def test_home():
    """Test home endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Tutor Backend Running"}

def test_health():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Backend healthy"}

def test_save_chat():
    """Test saving a chat message"""
    original_generate = ai_service.generate_ai_reply

    def mock_generate_ai_reply(model: str, message: str):
        return "This is a mock AI reply", 42, "gemini-2.0-flash"

    ai_service.generate_ai_reply = mock_generate_ai_reply
    try:
        chat_data = {
            "userId": "test_user_1",
            "topicId": "python_basics",
            "message": "What is Python?",
            "model": "gemini"
        }
        response = client.post("/api/v1/chat/", json=chat_data)
    finally:
        ai_service.generate_ai_reply = original_generate

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "chatId" in data["data"]
    assert data["data"]["reply"] == "This is a mock AI reply"
    assert data["data"]["model"] == "gemini-2.0-flash"
    assert data["data"]["tokensUsed"] == 42
    assert data["data"]["estimatedCost"] > 0

def test_get_chat_history():
    """Test retrieving chat history"""
    original_generate = ai_service.generate_ai_reply

    def mock_generate_ai_reply(model: str, message: str):
        return "History mock reply", 30, "gpt-4o-mini"

    ai_service.generate_ai_reply = mock_generate_ai_reply
    try:
        # First, save a chat
        chat_data = {
            "userId": "test_user_2",
            "topicId": "python_basics",
            "message": "Explain variables",
            "model": "openai"
        }
        client.post("/api/v1/chat/", json=chat_data)
    finally:
        ai_service.generate_ai_reply = original_generate
    
    # Then retrieve history
    response = client.get("/api/v1/chat/history/test_user_2")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0
    latest = data["data"][-1]
    assert latest["model"] == "gpt-4o-mini"
    assert latest["tokensUsed"] == 30
    assert "estimatedCost" in latest
