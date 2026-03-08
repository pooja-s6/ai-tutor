from sqlalchemy import Column, String, Text, DateTime, Integer, Float
from config.db import Base, engine
from datetime import datetime
import uuid

class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    topic_id = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    reply = Column(Text, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create all tables
Base.metadata.create_all(bind=engine)
