# backend/app/ai/__init__.py
"""
AI module package.
"""

from app.ai.ollama_client import ollama_client
from app.ai.insights_engine import generate_all_insights
from app.ai.chat_engine import chat_with_advisor