# backend/app/models/chat.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"
    __table_args__ = {'extend_existing': True}  # ← ADD THIS LINE

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chat_messages")

    def __repr__(self):
        return f"<Chat(user_id={self.user_id}, role={self.role})>"