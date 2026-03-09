from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from config.db import get_db
from models.chat_model import Chat
from services.ai_service import generate_ai_reply
from services.cost_service import estimate_cost

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    userId: str
    topicId: str
    message: str
    model: str

@router.post("/")
def save_chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Get AI reply and token usage
        ai_reply, tokens = generate_ai_reply(request.model, request.message)
        cost = estimate_cost(tokens)
        
        new_chat = Chat(
            user_id=request.userId,
            topic_id=request.topicId,
            message=request.message,
            reply=ai_reply,
            model=request.model,
            tokens_used=tokens,
            cost=cost
        )
        
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        
        return {
            "status": "success",
            "data": {
                "reply": ai_reply,
                "chatId": new_chat.chat_id,
                "tokensUsed": tokens,
                "estimatedCost": cost
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save chat: {str(e)}")

@router.get("/history/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    try:
        chats = db.query(Chat).filter(Chat.user_id == user_id).all()
        
        return {
            "status": "success",
            "data": [
                {
                    "chatId": chat.chat_id,
                    "message": chat.message,
                    "reply": chat.reply,
                    "timestamp": chat.timestamp.isoformat() if chat.timestamp else None
                }
                for chat in chats
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chat history: {str(e)}")
