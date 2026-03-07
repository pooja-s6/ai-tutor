import pytest
from fastapi.testclient import TestClient
from main import app

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
    chat_data = {
        "userId": "test_user_1",
        "topicId": "python_basics",
        "message": "What is Python?"
    }
    response = client.post("/chat/", json=chat_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "chatId" in data["data"]
    assert data["data"]["reply"] == "This is a mock AI reply"

def test_get_chat_history():
    """Test retrieving chat history"""
    # First, save a chat
    chat_data = {
        "userId": "test_user_2",
        "topicId": "python_basics",
        "message": "Explain variables"
    }
    client.post("/chat/", json=chat_data)
    
    # Then retrieve history
    response = client.get("/chat/history/test_user_2")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0
