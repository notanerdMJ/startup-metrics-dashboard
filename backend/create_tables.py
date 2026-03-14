import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, Base
from app.models.user import User
from app.models.raw_data import RawData
from app.models.metrics import CalculatedMetrics
from app.models.insight import AIInsight
from app.models.chat import ChatHistory

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables: {tables}")
print("✅ Done!")