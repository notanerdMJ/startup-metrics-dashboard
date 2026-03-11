# backend/app/models/raw_data.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class RawData(Base):
    __tablename__ = "raw_data"
    __table_args__ = {'extend_existing': True}  # ← ADD THIS LINE

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    customerid = Column(Integer, index=True)
    age = Column(Integer)
    gender = Column(String(50))
    income = Column(Float)
    campaignchannel = Column(String(100), index=True)
    campaigntype = Column(String(100))
    adspend = Column(Float)
    clickthroughrate = Column(Float)
    conversionrate = Column(Float)
    websitevisits = Column(Integer)
    pagespervisit = Column(Float)
    timeonsite = Column(Float)
    socialshares = Column(Integer)
    emailopens = Column(Integer)
    emailclicks = Column(Integer)
    previouspurchases = Column(Integer)
    loyaltypoints = Column(Integer)
    advertisingplatform = Column(String(100))
    advertisingtool = Column(String(100))
    conversion = Column(Integer, index=True)
    channel_used = Column(String(100))
    social_agg_conversion_rate = Column(Float)
    social_agg_acquisition_cost = Column(Float)

    loaded_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<RawData(id={self.id}, customerid={self.customerid})>"