# backend/app/routers/metrics.py
"""
Metrics API endpoints.
Uses the MetricsEngine for advanced calculations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.metrics_engine import MetricsEngine
from app.services.metrics_service import get_overall_summary

router = APIRouter()


@router.get("/summary")
async def metrics_summary(db: Session = Depends(get_db)):
    """Get overall metrics summary."""
    return get_overall_summary(db)


@router.get("/cac")
async def cac_metrics(db: Session = Depends(get_db)):
    """Get CAC analysis by channel."""
    engine = MetricsEngine(db)
    return {
        "by_channel": engine.get_cac_by_channel(),
        "by_campaign": engine.get_cac_by_campaign_type(),
        "by_platform": engine.get_cac_by_platform()
    }


@router.get("/ltv")
async def ltv_metrics(db: Session = Depends(get_db)):
    """Get LTV analysis by segments."""
    engine = MetricsEngine(db)
    return {
        "by_income_segment": engine.get_ltv_by_segment(),
        "by_age_group": engine.get_ltv_by_age_group(),
        "ltv_cac_ratio": engine.get_ltv_cac_by_channel()
    }


@router.get("/burn-rate")
async def burn_rate_metrics(db: Session = Depends(get_db)):
    """Get burn rate analysis."""
    engine = MetricsEngine(db)
    return {
        "by_channel": engine.get_burn_rate_by_channel(),
        "monthly_trend": engine.get_monthly_burn_trend()
    }


@router.get("/runway")
async def runway_metrics(db: Session = Depends(get_db)):
    """Get runway predictions."""
    engine = MetricsEngine(db)
    return {
        "scenarios": engine.get_runway_scenarios(),
        "timeline": engine.get_runway_timeline()
    }


@router.get("/funnel")
async def conversion_funnel(db: Session = Depends(get_db)):
    """Get conversion funnel analysis."""
    engine = MetricsEngine(db)
    return engine.get_conversion_funnel()


@router.get("/roi")
async def channel_roi(db: Session = Depends(get_db)):
    """Get channel ROI comparison."""
    engine = MetricsEngine(db)
    return engine.get_channel_roi()


@router.get("/complete")
async def complete_metrics(db: Session = Depends(get_db)):
    """Get ALL metrics in one API call."""
    engine = MetricsEngine(db)
    return engine.get_complete_dashboard()