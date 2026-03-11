# backend/app/services/metrics_engine.py
"""
Advanced Metrics Calculation Engine.
Provides deep financial analysis beyond basic ETL calculations.
This engine reads from the database and computes advanced insights.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from typing import List, Dict, Any
from app.models.raw_data import RawData
from app.models.metrics import CalculatedMetrics
import math


class MetricsEngine:
    """
    Central engine for all startup metrics calculations.
    Reads from PostgreSQL and returns formatted results.
    """

    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    #  CAC ANALYSIS
    # ============================================================

    def get_cac_by_channel(self) -> List[Dict[str, Any]]:
        """Get Customer Acquisition Cost broken down by campaign channel."""
        results = self.db.query(
            RawData.campaignchannel,
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.count(RawData.id).label("total_records"),
            func.avg(RawData.adspend).label("avg_spend")
        ).group_by(
            RawData.campaignchannel
        ).all()

        channels = []
        for r in results:
            cac = float(r.total_spend) / int(r.total_conversions) if r.total_conversions > 0 else 0
            channels.append({
                "channel": r.campaignchannel or "Unknown",
                "cac": round(cac, 2),
                "total_ad_spend": round(float(r.total_spend), 2),
                "customers_acquired": int(r.total_conversions),
                "total_records": int(r.total_records),
                "avg_spend_per_user": round(float(r.avg_spend), 2),
                "efficiency": "High" if cac < 100 else "Medium" if cac < 200 else "Low"
            })

        # Sort by CAC (lowest = best)
        channels.sort(key=lambda x: x["cac"])
        return channels

    def get_cac_by_campaign_type(self) -> List[Dict[str, Any]]:
        """Get CAC broken down by campaign type."""
        results = self.db.query(
            RawData.campaigntype,
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.avg(RawData.conversionrate).label("avg_conv_rate")
        ).group_by(
            RawData.campaigntype
        ).all()

        campaigns = []
        for r in results:
            cac = float(r.total_spend) / int(r.total_conversions) if r.total_conversions > 0 else 0
            campaigns.append({
                "campaign_type": r.campaigntype or "Unknown",
                "cac": round(cac, 2),
                "total_ad_spend": round(float(r.total_spend), 2),
                "customers_acquired": int(r.total_conversions),
                "avg_conversion_rate": round(float(r.avg_conv_rate or 0), 4)
            })

        campaigns.sort(key=lambda x: x["cac"])
        return campaigns

    def get_cac_by_platform(self) -> List[Dict[str, Any]]:
        """Get CAC broken down by advertising platform."""
        results = self.db.query(
            RawData.advertisingplatform,
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.avg(RawData.clickthroughrate).label("avg_ctr")
        ).group_by(
            RawData.advertisingplatform
        ).all()

        platforms = []
        for r in results:
            cac = float(r.total_spend) / int(r.total_conversions) if r.total_conversions > 0 else 0
            platforms.append({
                "platform": r.advertisingplatform or "Unknown",
                "cac": round(cac, 2),
                "total_ad_spend": round(float(r.total_spend), 2),
                "customers_acquired": int(r.total_conversions),
                "avg_ctr": round(float(r.avg_ctr or 0), 4)
            })

        platforms.sort(key=lambda x: x["cac"])
        return platforms

    # ============================================================
    #  LTV ANALYSIS
    # ============================================================

    def get_ltv_by_segment(self) -> List[Dict[str, Any]]:
        """Calculate LTV across different customer segments."""
        # Income-based segments
        income_segments = self.db.query(
            case(
                (RawData.income < 30000, "Low Income (<$30K)"),
                (RawData.income < 60000, "Mid Income ($30K-$60K)"),
                (RawData.income < 90000, "High Income ($60K-$90K)"),
                else_="Premium (>$90K)"
            ).label("segment"),
            func.avg(RawData.income).label("avg_income"),
            func.avg(RawData.previouspurchases).label("avg_purchases"),
            func.avg(RawData.loyaltypoints).label("avg_loyalty"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.count(RawData.id).label("total_customers")
        ).group_by("segment").all()

        segments = []
        for s in income_segments:
            avg_income = float(s.avg_income or 0)
            avg_purchases = float(s.avg_purchases or 0)
            avg_loyalty = float(s.avg_loyalty or 0)

            # LTV Formula
            purchase_factor = avg_purchases * 0.15 if avg_purchases > 0 else 1
            retention_factor = 1 + (avg_loyalty / 1000) if avg_loyalty > 0 else 1
            ltv = avg_income * purchase_factor * retention_factor * 0.01

            segments.append({
                "segment": s.segment,
                "ltv": round(ltv, 2),
                "avg_income": round(avg_income, 2),
                "avg_purchases": round(avg_purchases, 1),
                "avg_loyalty_points": round(avg_loyalty, 0),
                "total_customers": int(s.total_customers),
                "total_conversions": int(s.total_conversions),
                "conversion_rate": round(int(s.total_conversions) / int(s.total_customers), 4) if s.total_customers > 0 else 0
            })

        segments.sort(key=lambda x: x["ltv"], reverse=True)
        return segments

    def get_ltv_by_age_group(self) -> List[Dict[str, Any]]:
        """Calculate LTV by age groups."""
        age_segments = self.db.query(
            case(
                (RawData.age < 25, "18-24"),
                (RawData.age < 35, "25-34"),
                (RawData.age < 45, "35-44"),
                (RawData.age < 55, "45-54"),
                else_="55+"
            ).label("age_group"),
            func.avg(RawData.income).label("avg_income"),
            func.avg(RawData.previouspurchases).label("avg_purchases"),
            func.avg(RawData.loyaltypoints).label("avg_loyalty"),
            func.count(RawData.id).label("count")
        ).group_by("age_group").all()

        groups = []
        for g in age_segments:
            avg_income = float(g.avg_income or 0)
            avg_purchases = float(g.avg_purchases or 0)
            avg_loyalty = float(g.avg_loyalty or 0)

            purchase_factor = avg_purchases * 0.15 if avg_purchases > 0 else 1
            retention_factor = 1 + (avg_loyalty / 1000) if avg_loyalty > 0 else 1
            ltv = avg_income * purchase_factor * retention_factor * 0.01

            groups.append({
                "age_group": g.age_group,
                "ltv": round(ltv, 2),
                "avg_income": round(avg_income, 2),
                "avg_purchases": round(avg_purchases, 1),
                "customer_count": int(g.count)
            })

        return groups

    # ============================================================
    #  LTV:CAC RATIO ANALYSIS
    # ============================================================

    def get_ltv_cac_by_channel(self) -> List[Dict[str, Any]]:
        """Calculate LTV:CAC ratio for each channel."""
        results = self.db.query(
            RawData.campaignchannel,
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.avg(RawData.income).label("avg_income"),
            func.avg(RawData.previouspurchases).label("avg_purchases"),
            func.avg(RawData.loyaltypoints).label("avg_loyalty")
        ).group_by(RawData.campaignchannel).all()

        channels = []
        for r in results:
            # CAC
            cac = float(r.total_spend) / int(r.total_conversions) if r.total_conversions > 0 else 0

            # LTV
            avg_income = float(r.avg_income or 0)
            avg_purchases = float(r.avg_purchases or 0)
            avg_loyalty = float(r.avg_loyalty or 0)
            purchase_factor = avg_purchases * 0.15 if avg_purchases > 0 else 1
            retention_factor = 1 + (avg_loyalty / 1000) if avg_loyalty > 0 else 1
            ltv = avg_income * purchase_factor * retention_factor * 0.01

            # Ratio
            ratio = ltv / cac if cac > 0 else 0

            # Health assessment
            if ratio >= 5:
                health = "Excellent"
            elif ratio >= 3:
                health = "Healthy"
            elif ratio >= 1:
                health = "Warning"
            else:
                health = "Critical"

            channels.append({
                "channel": r.campaignchannel or "Unknown",
                "ltv": round(ltv, 2),
                "cac": round(cac, 2),
                "ltv_cac_ratio": round(ratio, 2),
                "health": health
            })

        channels.sort(key=lambda x: x["ltv_cac_ratio"], reverse=True)
        return channels

    # ============================================================
    #  BURN RATE ANALYSIS
    # ============================================================

    def get_burn_rate_by_channel(self) -> List[Dict[str, Any]]:
        """Calculate burn rate (expenses - revenue) per channel."""
        results = self.db.query(
            RawData.campaignchannel,
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.avg(RawData.income).label("avg_income"),
            func.count(RawData.id).label("total_records")
        ).group_by(RawData.campaignchannel).all()

        channels = []
        for r in results:
            total_spend = float(r.total_spend)
            avg_income = float(r.avg_income or 0)
            conversions = int(r.total_conversions)

            # Monthly figures (divide annual by 12)
            monthly_expenses = total_spend / 12
            monthly_revenue = (conversions * avg_income * 0.05) / 12
            monthly_burn = monthly_expenses - monthly_revenue

            channels.append({
                "channel": r.campaignchannel or "Unknown",
                "monthly_revenue": round(monthly_revenue, 2),
                "monthly_expenses": round(monthly_expenses, 2),
                "burn_rate": round(monthly_burn, 2),
                "is_profitable": monthly_revenue > monthly_expenses
            })

        channels.sort(key=lambda x: x["burn_rate"], reverse=True)
        return channels

    def get_monthly_burn_trend(self) -> List[Dict[str, Any]]:
        """Simulate monthly burn rate trend over 12 months."""
        overall = self.db.query(
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.avg(RawData.income).label("avg_income")
        ).first()

        if not overall or not overall.total_spend:
            return []

        total_spend = float(overall.total_spend)
        total_conv = int(overall.total_conversions or 0)
        avg_income = float(overall.avg_income or 0)

        base_monthly_expense = total_spend / 12
        base_monthly_revenue = (total_conv * avg_income * 0.05) / 12

        months = []
        month_names = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]

        for i, month in enumerate(month_names):
            # Simulate growth: expenses grow 2% monthly, revenue grows 5% monthly
            expense_factor = 1 + (i * 0.02)
            revenue_factor = 1 + (i * 0.05)

            expenses = base_monthly_expense * expense_factor
            revenue = base_monthly_revenue * revenue_factor
            burn = expenses - revenue

            months.append({
                "month": month,
                "month_number": i + 1,
                "revenue": round(revenue, 2),
                "expenses": round(expenses, 2),
                "burn_rate": round(burn, 2),
                "cumulative_burn": round(burn * (i + 1), 2)
            })

        return months

    # ============================================================
    #  RUNWAY PREDICTIONS
    # ============================================================

    def get_runway_scenarios(self) -> List[Dict[str, Any]]:
        """Calculate runway under different scenarios."""
        overall = self.db.query(
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.avg(RawData.income).label("avg_income")
        ).first()

        if not overall or not overall.total_spend:
            return []

        total_spend = float(overall.total_spend)
        total_conv = int(overall.total_conversions or 0)
        avg_income = float(overall.avg_income or 0)

        monthly_expense = total_spend / 12
        monthly_revenue = (total_conv * avg_income * 0.05) / 12
        monthly_burn = monthly_expense - monthly_revenue

        simulated_bank = 1000000  # $1M

        scenarios = [
            {
                "scenario": "Current Pace",
                "description": "No changes to spending or revenue",
                "monthly_burn": round(monthly_burn, 2),
                "monthly_revenue": round(monthly_revenue, 2),
                "monthly_expenses": round(monthly_expense, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / monthly_burn, 1) if monthly_burn > 0 else 999,
                "risk_level": "high" if (simulated_bank / monthly_burn if monthly_burn > 0 else 999) < 6 else "medium" if (simulated_bank / monthly_burn if monthly_burn > 0 else 999) < 12 else "low"
            },
            {
                "scenario": "20% Cost Reduction",
                "description": "Cut marketing spend by 20%",
                "monthly_burn": round(monthly_expense * 0.8 - monthly_revenue, 2),
                "monthly_revenue": round(monthly_revenue, 2),
                "monthly_expenses": round(monthly_expense * 0.8, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / (monthly_expense * 0.8 - monthly_revenue), 1) if (monthly_expense * 0.8 - monthly_revenue) > 0 else 999,
                "risk_level": "medium"
            },
            {
                "scenario": "50% Cost Reduction",
                "description": "Aggressive cost cutting",
                "monthly_burn": round(monthly_expense * 0.5 - monthly_revenue, 2),
                "monthly_revenue": round(monthly_revenue, 2),
                "monthly_expenses": round(monthly_expense * 0.5, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / (monthly_expense * 0.5 - monthly_revenue), 1) if (monthly_expense * 0.5 - monthly_revenue) > 0 else 999,
                "risk_level": "low"
            },
            {
                "scenario": "Revenue 2x Growth",
                "description": "Double the conversion revenue",
                "monthly_burn": round(monthly_expense - monthly_revenue * 2, 2),
                "monthly_revenue": round(monthly_revenue * 2, 2),
                "monthly_expenses": round(monthly_expense, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / (monthly_expense - monthly_revenue * 2), 1) if (monthly_expense - monthly_revenue * 2) > 0 else 999,
                "risk_level": "low"
            },
            {
                "scenario": "Worst Case",
                "description": "Revenue drops 50%, costs rise 20%",
                "monthly_burn": round(monthly_expense * 1.2 - monthly_revenue * 0.5, 2),
                "monthly_revenue": round(monthly_revenue * 0.5, 2),
                "monthly_expenses": round(monthly_expense * 1.2, 2),
                "bank_balance": simulated_bank,
                "runway_months": round(simulated_bank / (monthly_expense * 1.2 - monthly_revenue * 0.5), 1) if (monthly_expense * 1.2 - monthly_revenue * 0.5) > 0 else 999,
                "risk_level": "critical"
            },
        ]

        return scenarios

    def get_runway_timeline(self) -> List[Dict[str, Any]]:
        """Generate month-by-month runway countdown."""
        overall = self.db.query(
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.avg(RawData.income).label("avg_income")
        ).first()

        if not overall or not overall.total_spend:
            return []

        total_spend = float(overall.total_spend)
        total_conv = int(overall.total_conversions or 0)
        avg_income = float(overall.avg_income or 0)

        monthly_expense = total_spend / 12
        monthly_revenue = (total_conv * avg_income * 0.05) / 12

        bank_balance = 1000000
        timeline = []

        for month in range(1, 25):  # 24 months forecast
            revenue = monthly_revenue * (1 + month * 0.03)  # 3% growth
            expenses = monthly_expense * (1 + month * 0.01)  # 1% growth
            burn = expenses - revenue
            bank_balance -= burn

            timeline.append({
                "month": month,
                "bank_balance": round(max(bank_balance, 0), 2),
                "monthly_revenue": round(revenue, 2),
                "monthly_expenses": round(expenses, 2),
                "monthly_burn": round(burn, 2),
                "is_alive": bank_balance > 0
            })

            if bank_balance <= 0:
                break

        return timeline

    # ============================================================
    #  CONVERSION FUNNEL
    # ============================================================

    def get_conversion_funnel(self) -> List[Dict[str, Any]]:
        """Analyze the conversion funnel."""
        total_users = self.db.query(func.count(RawData.id)).scalar() or 0
        total_visits = self.db.query(func.sum(RawData.websitevisits)).scalar() or 0
        total_email_opens = self.db.query(func.sum(RawData.emailopens)).scalar() or 0
        total_email_clicks = self.db.query(func.sum(RawData.emailclicks)).scalar() or 0
        total_conversions = self.db.query(func.sum(RawData.conversion)).scalar() or 0

        funnel = [
            {
                "stage": "Total Audience",
                "count": int(total_users),
                "percentage": 100.0
            },
            {
                "stage": "Website Visitors",
                "count": int(total_visits),
                "percentage": round((int(total_visits) / int(total_users) * 100) if total_users > 0 else 0, 1)
            },
            {
                "stage": "Email Opens",
                "count": int(total_email_opens),
                "percentage": round((int(total_email_opens) / int(total_users) * 100) if total_users > 0 else 0, 1)
            },
            {
                "stage": "Email Clicks",
                "count": int(total_email_clicks),
                "percentage": round((int(total_email_clicks) / int(total_users) * 100) if total_users > 0 else 0, 1)
            },
            {
                "stage": "Conversions",
                "count": int(total_conversions),
                "percentage": round((int(total_conversions) / int(total_users) * 100) if total_users > 0 else 0, 1)
            },
        ]

        return funnel

    # ============================================================
    #  CHANNEL ROI COMPARISON
    # ============================================================

    def get_channel_roi(self) -> List[Dict[str, Any]]:
        """Calculate ROI for each marketing channel."""
        results = self.db.query(
            RawData.campaignchannel,
            func.sum(RawData.adspend).label("total_spend"),
            func.sum(RawData.conversion).label("total_conversions"),
            func.avg(RawData.income).label("avg_income"),
            func.avg(RawData.conversionrate).label("avg_conv_rate"),
            func.avg(RawData.clickthroughrate).label("avg_ctr")
        ).group_by(RawData.campaignchannel).all()

        channels = []
        for r in results:
            total_spend = float(r.total_spend)
            conversions = int(r.total_conversions)
            avg_income = float(r.avg_income or 0)

            estimated_revenue = conversions * avg_income * 0.05
            roi = ((estimated_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0

            channels.append({
                "channel": r.campaignchannel or "Unknown",
                "total_spend": round(total_spend, 2),
                "estimated_revenue": round(estimated_revenue, 2),
                "roi_percentage": round(roi, 1),
                "conversions": conversions,
                "avg_conversion_rate": round(float(r.avg_conv_rate or 0), 4),
                "avg_ctr": round(float(r.avg_ctr or 0), 4),
                "is_positive_roi": roi > 0
            })

        channels.sort(key=lambda x: x["roi_percentage"], reverse=True)
        return channels

    # ============================================================
    #  COMPLETE DASHBOARD DATA
    # ============================================================

    def get_complete_dashboard(self) -> Dict[str, Any]:
        """Get all dashboard data in one call."""
        return {
            "cac_by_channel": self.get_cac_by_channel(),
            "cac_by_campaign": self.get_cac_by_campaign_type(),
            "cac_by_platform": self.get_cac_by_platform(),
            "ltv_by_segment": self.get_ltv_by_segment(),
            "ltv_by_age": self.get_ltv_by_age_group(),
            "ltv_cac_ratio": self.get_ltv_cac_by_channel(),
            "burn_rate_by_channel": self.get_burn_rate_by_channel(),
            "monthly_burn_trend": self.get_monthly_burn_trend(),
            "runway_scenarios": self.get_runway_scenarios(),
            "runway_timeline": self.get_runway_timeline(),
            "conversion_funnel": self.get_conversion_funnel(),
            "channel_roi": self.get_channel_roi()
        }