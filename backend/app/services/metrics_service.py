# backend/app/services/metrics_service.py
"""
Metrics calculation business logic.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.models.metrics import CalculatedMetrics
from app.models.raw_data import RawData


def get_overall_summary(db: Session) -> Dict[str, Any]:
    """Get the overall metrics summary."""
    try:
        # First try calculated metrics
        overall = db.query(CalculatedMetrics).filter(
            CalculatedMetrics.segment_type == "overall",
            CalculatedMetrics.segment_value == "all"
        ).first()

        if overall:
            return {
                "total_records": overall.total_customers or 0,
                "total_ad_spend": round(float(overall.total_ad_spend or 0), 2),
                "total_conversions": int(overall.total_conversions or 0),
                "overall_cac": round(float(overall.cac or 0), 2),
                "average_ltv": round(float(overall.estimated_ltv or 0), 2),
                "ltv_cac_ratio": round(float(overall.ltv_cac_ratio or 0), 2),
                "estimated_burn_rate": round(float(overall.burn_rate or 0), 2),
                "estimated_runway_months": round(float(overall.estimated_runway_months or 0), 1),
                "is_healthy": float(overall.ltv_cac_ratio or 0) >= 3.0
            }

        # Fallback: calculate from raw data
        return calculate_from_raw(db)

    except Exception as e:
        print(f"Error in get_overall_summary: {e}")
        return calculate_from_raw(db)


def calculate_from_raw(db: Session) -> Dict[str, Any]:
    """Calculate metrics directly from raw data."""
    try:
        total_records = db.query(func.count(RawData.id)).scalar() or 0

        if total_records == 0:
            return {
                "total_records": 0,
                "total_ad_spend": 0,
                "total_conversions": 0,
                "overall_cac": 0,
                "average_ltv": 0,
                "ltv_cac_ratio": 0,
                "estimated_burn_rate": 0,
                "estimated_runway_months": 0,
                "is_healthy": False
            }

        total_ad_spend = float(db.query(func.sum(RawData.adspend)).scalar() or 0)
        total_conversions = int(db.query(func.sum(RawData.conversion)).scalar() or 0)
        avg_income = float(db.query(func.avg(RawData.income)).scalar() or 0)
        avg_purchases = float(db.query(func.avg(RawData.previouspurchases)).scalar() or 0)

        cac = total_ad_spend / total_conversions if total_conversions > 0 else 0
        ltv = avg_income * (avg_purchases * 0.1) if avg_purchases > 0 else 0
        ltv_cac_ratio = ltv / cac if cac > 0 else 0
        burn_rate = total_ad_spend / 12
        runway = 1000000 / burn_rate if burn_rate > 0 else 0

        return {
            "total_records": total_records,
            "total_ad_spend": round(total_ad_spend, 2),
            "total_conversions": total_conversions,
            "overall_cac": round(cac, 2),
            "average_ltv": round(ltv, 2),
            "ltv_cac_ratio": round(ltv_cac_ratio, 2),
            "estimated_burn_rate": round(burn_rate, 2),
            "estimated_runway_months": round(min(runway, 999), 1),
            "is_healthy": ltv_cac_ratio >= 3.0
        }

    except Exception as e:
        print(f"Error in calculate_from_raw: {e}")
        return {
            "total_records": 0,
            "total_ad_spend": 0,
            "total_conversions": 0,
            "overall_cac": 0,
            "average_ltv": 0,
            "ltv_cac_ratio": 0,
            "estimated_burn_rate": 0,
            "estimated_runway_months": 0,
            "is_healthy": False
        }


def get_channel_metrics(db: Session) -> List[Dict[str, Any]]:
    """Get metrics broken down by campaign channel."""
    try:
        channels = db.query(CalculatedMetrics).filter(
            CalculatedMetrics.segment_type == "channel"
        ).all()

        if channels:
            return [
                {
                    "channel": ch.segment_value or "Unknown",
                    "ad_spend": round(float(ch.total_ad_spend or 0), 2),
                    "conversions": int(ch.total_conversions or 0),
                    "cac": round(float(ch.cac or 0), 2),
                    "conversion_rate": round(float(ch.avg_conversion_rate or 0), 4),
                    "ltv": round(float(ch.estimated_ltv or 0), 2),
                    "ltv_cac_ratio": round(float(ch.ltv_cac_ratio or 0), 2),
                    "is_profitable": bool(ch.is_profitable)
                }
                for ch in channels
            ]

        return calculate_channel_from_raw(db)

    except Exception as e:
        print(f"Error in get_channel_metrics: {e}")
        return []


def calculate_channel_from_raw(db: Session) -> List[Dict[str, Any]]:
    """Calculate channel metrics from raw data."""
    try:
        channels = db.query(
            RawData.campaignchannel,
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conv"),
            func.avg(RawData.conversionrate).label("avg_conv_rate"),
            func.avg(RawData.income).label("avg_income"),
            func.avg(RawData.previouspurchases).label("avg_purchases"),
            func.count(RawData.id).label("total_records")
        ).group_by(RawData.campaignchannel).all()

        results = []
        for ch in channels:
            total_spend = float(ch.total_spend or 0)
            total_conv = int(ch.total_conv or 0)
            avg_income = float(ch.avg_income or 0)
            avg_purchases = float(ch.avg_purchases or 0)

            cac = total_spend / total_conv if total_conv > 0 else 0
            ltv = avg_income * (avg_purchases * 0.1) if avg_purchases > 0 else 0
            ltv_cac_ratio = ltv / cac if cac > 0 else 0

            results.append({
                "channel": ch.campaignchannel or "Unknown",
                "ad_spend": round(total_spend, 2),
                "conversions": total_conv,
                "cac": round(cac, 2),
                "conversion_rate": round(float(ch.avg_conv_rate or 0), 4),
                "ltv": round(ltv, 2),
                "ltv_cac_ratio": round(ltv_cac_ratio, 2),
                "is_profitable": ltv_cac_ratio >= 3.0
            })

        return results

    except Exception as e:
        print(f"Error in calculate_channel_from_raw: {e}")
        return []


def get_cac_data(db: Session) -> List[Dict[str, Any]]:
    """Get CAC data for charts."""
    channels = get_channel_metrics(db)
    return [
        {
            "channel": ch["channel"],
            "cac": ch["cac"],
            "ad_spend": ch["ad_spend"],
            "customers_acquired": ch["conversions"]
        }
        for ch in channels
    ]


def get_ltv_data(db: Session) -> List[Dict[str, Any]]:
    """Get LTV data by income groups."""
    try:
        from sqlalchemy import case
        income_groups = db.query(
            case(
                (RawData.income < 30000, "Low Income"),
                (RawData.income < 60000, "Mid Income"),
                (RawData.income < 90000, "High Income"),
                else_="Premium"
            ).label("segment"),
            func.avg(RawData.income).label("avg_income"),
            func.avg(RawData.previouspurchases).label("avg_purchases"),
            func.count(RawData.id).label("count")
        ).group_by("segment").all()

        results = []
        for group in income_groups:
            avg_income = float(group.avg_income or 0)
            avg_purchases = float(group.avg_purchases or 0)
            ltv = avg_income * (avg_purchases * 0.1)
            results.append({
                "segment": group.segment,
                "ltv": round(ltv, 2),
                "avg_purchases": round(avg_purchases, 1),
                "avg_income": round(avg_income, 2)
            })

        return results

    except Exception as e:
        print(f"Error in get_ltv_data: {e}")
        return []


def get_burn_rate_data(db: Session) -> List[Dict[str, Any]]:
    """Get burn rate data by channel."""
    try:
        channels = get_channel_metrics(db)
        results = []
        for ch in channels:
            revenue = ch["ltv"] * ch["conversions"] * 0.1
            expenses = ch["ad_spend"]
            burn = expenses - revenue

            results.append({
                "channel": ch["channel"],
                "revenue": round(revenue, 2),
                "expenses": round(expenses, 2),
                "burn_rate": round(burn, 2)
            })

        return results

    except Exception as e:
        print(f"Error in get_burn_rate_data: {e}")
        return []


def get_runway_data(db: Session) -> List[Dict[str, Any]]:
    """Get runway predictions."""
    try:
        summary = get_overall_summary(db)
        monthly_burn = summary["estimated_burn_rate"]

        if monthly_burn <= 0:
            monthly_burn = 1

        simulated_bank = 1000000

        scenarios = [
            {
                "scenario": "Current Pace",
                "burn_rate": round(monthly_burn, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / monthly_burn, 1)
            },
            {
                "scenario": "20% Cost Cut",
                "burn_rate": round(monthly_burn * 0.8, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / (monthly_burn * 0.8), 1)
            },
            {
                "scenario": "50% Cost Cut",
                "burn_rate": round(monthly_burn * 0.5, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / (monthly_burn * 0.5), 1)
            },
            {
                "scenario": "Revenue Doubles",
                "burn_rate": round(monthly_burn * 0.6, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / (monthly_burn * 0.6), 1)
            },
        ]

        return scenarios

    except Exception as e:
        print(f"Error in get_runway_data: {e}")
        return []