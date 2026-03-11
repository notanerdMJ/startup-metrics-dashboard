# backend/app/routers/dashboard.py
"""
Dashboard API endpoints.
Combines metrics engine + dashboard service for frontend.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.dashboard_service import get_dashboard_cards, get_health_score
from app.services.metrics_engine import MetricsEngine
from app.services.metrics_service import get_overall_summary

router = APIRouter()


@router.get("/cards")
async def dashboard_cards(db: Session = Depends(get_db)):
    """Get summary cards for dashboard overview."""
    return get_dashboard_cards(db)


@router.get("/health")
async def dashboard_health(db: Session = Depends(get_db)):
    """Get overall startup health score."""
    return get_health_score(db)


@router.get("/charts")
async def dashboard_charts(db: Session = Depends(get_db)):
    """Get all chart data in one call."""
    engine = MetricsEngine(db)
    return {
        "cac_by_channel": engine.get_cac_by_channel(),
        "ltv_by_segment": engine.get_ltv_by_segment(),
        "burn_rate_trend": engine.get_monthly_burn_trend(),
        "runway_timeline": engine.get_runway_timeline(),
        "channel_roi": engine.get_channel_roi(),
        "conversion_funnel": engine.get_conversion_funnel()
    }


@router.get("/overview")
async def dashboard_overview(db: Session = Depends(get_db)):
    """Complete dashboard data in one call."""
    engine = MetricsEngine(db)
    return {
        "cards": get_dashboard_cards(db),
        "health": get_health_score(db),
        "summary": get_overall_summary(db),
        "ltv_cac_ratio": engine.get_ltv_cac_by_channel(),
        "runway_scenarios": engine.get_runway_scenarios()
    }