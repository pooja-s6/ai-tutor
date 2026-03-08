from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from config.db import get_db
from models.chat_model import Chat

router = APIRouter(prefix="/usage", tags=["Usage"])

@router.get("/{user_id}")
def get_usage(user_id: str, db: Session = Depends(get_db)):
    """
    Get usage statistics for a specific user
    
    Returns:
        - Total messages sent
        - Total tokens used
        - Estimated total cost
    """
    try:
        # Calculate total tokens used
        total_tokens = db.query(func.sum(Chat.tokens_used)).filter(Chat.user_id == user_id).scalar() or 0
        
        # Calculate total cost
        total_cost = db.query(func.sum(Chat.cost)).filter(Chat.user_id == user_id).scalar() or 0
        
        # Count total messages
        total_messages = db.query(Chat).filter(Chat.user_id == user_id).count()
        
        return {
            "status": "success",
            "data": {
                "userId": user_id,
                "totalMessages": total_messages,
                "tokensUsed": int(total_tokens),
                "estimatedCost": round(total_cost, 6)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve usage: {str(e)}")
