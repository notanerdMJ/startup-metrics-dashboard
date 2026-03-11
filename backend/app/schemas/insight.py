# backend/app/schemas/insight.py
"""
Pydantic schemas for AI Insights API responses.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class InsightResponse(BaseModel):
    id: int
    insight_type: str
    segment: str
    insight_text: str
    severity: str
    recommendation: Optional[str]
    metric_value: Optional[str]
    generated_at: datetime

    class Config:
        from_attributes = True


class InsightListResponse(BaseModel):
    insights: List[InsightResponse]
    total: int

    class Config:
        from_attributes = True