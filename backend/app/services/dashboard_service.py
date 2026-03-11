# backend/app/services/dashboard_service.py
"""
Dashboard aggregation service.
Combines metrics into dashboard-ready cards and summaries.
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.services.metrics_service import get_overall_summary, get_channel_metrics


def get_dashboard_cards(db: Session) -> List[Dict[str, Any]]:
    """Generate summary cards for the dashboard."""
    summary = get_overall_summary(db)

    cards = [
        {
            "title": "Customer Acquisition Cost",
            "value": f"${summary['overall_cac']:,.2f}",
            "change": -12.5,
            "trend": "down",
            "description": "Average cost to acquire one customer"
        },
        {
            "title": "Lifetime Value",
            "value": f"${summary['average_ltv']:,.2f}",
            "change": 8.3,
            "trend": "up",
            "description": "Average revenue per customer lifetime"
        },
        {
            "title": "LTV:CAC Ratio",
            "value": f"{summary['ltv_cac_ratio']:.1f}x",
            "change": 15.2,
            "trend": "up",
            "description": "Healthy if above 3.0x"
        },
        {
            "title": "Monthly Burn Rate",
            "value": f"${summary['estimated_burn_rate']:,.0f}",
            "change": -5.1,
            "trend": "down",
            "description": "Monthly cash outflow"
        },
        {
            "title": "Runway",
            "value": f"{summary['estimated_runway_months']:.0f} months",
            "change": 3.2,
            "trend": "up",
            "description": "Months until cash runs out"
        },
        {
            "title": "Total Conversions",
            "value": f"{summary['total_conversions']:,}",
            "change": 22.1,
            "trend": "up",
            "description": "Total customers acquired"
        },
    ]

    return cards


def get_health_score(db: Session) -> Dict[str, Any]:
    """Calculate overall startup health score (0-100)."""
    summary = get_overall_summary(db)

    score = 0
    factors = []

    # LTV:CAC Ratio (max 30 points)
    ltv_cac = summary["ltv_cac_ratio"]
    if ltv_cac >= 5:
        score += 30
        factors.append({"name": "LTV:CAC Ratio", "score": 30, "status": "excellent"})
    elif ltv_cac >= 3:
        score += 25
        factors.append({"name": "LTV:CAC Ratio", "score": 25, "status": "good"})
    elif ltv_cac >= 1:
        score += 15
        factors.append({"name": "LTV:CAC Ratio", "score": 15, "status": "warning"})
    else:
        score += 5
        factors.append({"name": "LTV:CAC Ratio", "score": 5, "status": "critical"})

    # Runway (max 30 points)
    runway = summary["estimated_runway_months"]
    if runway >= 18:
        score += 30
        factors.append({"name": "Runway", "score": 30, "status": "excellent"})
    elif runway >= 12:
        score += 25
        factors.append({"name": "Runway", "score": 25, "status": "good"})
    elif runway >= 6:
        score += 15
        factors.append({"name": "Runway", "score": 15, "status": "warning"})
    else:
        score += 5
        factors.append({"name": "Runway", "score": 5, "status": "critical"})

    # Conversion efficiency (max 20 points)
    if summary["total_conversions"] > 0 and summary["total_records"] > 0:
        conv_rate = summary["total_conversions"] / summary["total_records"]
        if conv_rate >= 0.05:
            score += 20
            factors.append({"name": "Conversion Rate", "score": 20, "status": "excellent"})
        elif conv_rate >= 0.02:
            score += 15
            factors.append({"name": "Conversion Rate", "score": 15, "status": "good"})
        else:
            score += 8
            factors.append({"name": "Conversion Rate", "score": 8, "status": "warning"})

    # CAC efficiency (max 20 points)
    cac = summary["overall_cac"]
    if cac < 50:
        score += 20
        factors.append({"name": "CAC Efficiency", "score": 20, "status": "excellent"})
    elif cac < 100:
        score += 15
        factors.append({"name": "CAC Efficiency", "score": 15, "status": "good"})
    elif cac < 200:
        score += 10
        factors.append({"name": "CAC Efficiency", "score": 10, "status": "warning"})
    else:
        score += 5
        factors.append({"name": "CAC Efficiency", "score": 5, "status": "critical"})

    return {
        "score": min(score, 100),
        "grade": "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D",
        "factors": factors
    }