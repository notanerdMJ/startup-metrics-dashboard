# backend/app/models/__init__.py
"""
Central model registry.
Import all models here so SQLAlchemy and Alembic can discover them.
"""

from app.models.user import User
from app.models.raw_data import RawData
from app.models.metrics import CalculatedMetrics
from app.models.insight import AIInsight
from app.models.chat import ChatHistory

# This list makes it easy to reference all models
__all__ = [
    "User",
    "RawData",
    "CalculatedMetrics",
    "AIInsight",
    "ChatHistory",
]