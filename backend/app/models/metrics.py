# backend/app/models/metrics.py

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class CalculatedMetrics(Base):
    __tablename__ = "calculated_metrics"
    __table_args__ = {'extend_existing': True}  # ← ADD THIS LINE

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    segment_type = Column(String(50), index=True)
    segment_value = Column(String(100), index=True)

    total_ad_spend = Column(Float, default=0)
    total_customers = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    cac = Column(Float, default=0)
    estimated_ltv = Column(Float, default=0)
    ltv_cac_ratio = Column(Float, default=0)

    estimated_revenue = Column(Float, default=0)
    total_expenses = Column(Float, default=0)
    profit_loss = Column(Float, default=0)
    is_profitable = Column(Boolean, default=False)

    burn_rate = Column(Float, default=0)
    estimated_runway_months = Column(Float, default=0)

    avg_conversion_rate = Column(Float, default=0)
    avg_click_through_rate = Column(Float, default=0)
    cost_per_click = Column(Float, default=0)

    avg_income = Column(Float, default=0)
    avg_previous_purchases = Column(Float, default=0)
    avg_loyalty_points = Column(Float, default=0)
    avg_website_visits = Column(Float, default=0)
    avg_time_on_site = Column(Float, default=0)

    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Metrics(segment={self.segment_type}:{self.segment_value}, CAC={self.cac})>"