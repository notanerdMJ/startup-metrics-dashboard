# backend/app/schemas/metrics.py
"""
Pydantic schemas for Metrics API responses.
These define the exact JSON shape the frontend receives.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MetricsSummaryResponse(BaseModel):
    total_records: int
    total_ad_spend: float
    total_conversions: int
    overall_cac: float
    average_ltv: float
    ltv_cac_ratio: float
    estimated_burn_rate: float
    estimated_runway_months: float
    is_healthy: bool

    class Config:
        from_attributes = True


class ChannelMetricsResponse(BaseModel):
    segment_value: str
    total_ad_spend: float
    total_conversions: int
    cac: float
    avg_conversion_rate: float
    estimated_ltv: float
    ltv_cac_ratio: float
    is_profitable: bool

    class Config:
        from_attributes = True


class CACDataResponse(BaseModel):
    channel: str
    cac: float
    ad_spend: float
    customers_acquired: int

    class Config:
        from_attributes = True


class LTVDataResponse(BaseModel):
    segment: str
    ltv: float
    avg_purchases: float
    avg_income: float

    class Config:
        from_attributes = True


class BurnRateDataResponse(BaseModel):
    channel: str
    revenue: float
    expenses: float
    burn_rate: float

    class Config:
        from_attributes = True


class RunwayDataResponse(BaseModel):
    scenario: str
    runway_months: float
    burn_rate: float
    bank_balance: float

    class Config:
        from_attributes = True


class DashboardCardResponse(BaseModel):
    title: str
    value: str
    change: float
    trend: str  # "up", "down", "neutral"
    description: str

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    cards: List[DashboardCardResponse]
    summary: MetricsSummaryResponse
    channel_metrics: List[ChannelMetricsResponse]

    class Config:
        from_attributes = True