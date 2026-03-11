# backend/app/models/insight.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class AIInsight(Base):
    __tablename__ = "ai_insights"
    __table_args__ = {'extend_existing': True}  # ← ADD THIS LINE

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    insight_type = Column(String(50), index=True)
    segment = Column(String(100), default="overall")
    insight_text = Column(Text, nullable=False)
    severity = Column(String(20), default="warning")
    recommendation = Column(Text)
    metric_value = Column(String(100))

    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<AIInsight(type={self.insight_type}, severity={self.severity})>"