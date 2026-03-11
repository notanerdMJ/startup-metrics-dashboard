# backend/app/schemas/chat.py
"""
Pydantic schemas for AI Chat API.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatMessageRequest(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]
    total: int

    class Config:
        from_attributes = True