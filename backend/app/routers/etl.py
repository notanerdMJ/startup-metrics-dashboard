# backend/app/routers/etl.py
"""
ETL Pipeline API endpoints.
Trigger data processing and check status.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.raw_data import RawData
from app.models.metrics import CalculatedMetrics

router = APIRouter()


@router.post("/run")
async def run_etl(db: Session = Depends(get_db)):
    """
    Trigger the ETL pipeline.
    Reads CSV → Transforms → Loads into database.
    We'll implement the actual pipeline in Phase 5.
    """
    try:
        from app.etl.pipeline import run_pipeline
        result = run_pipeline(db)
        return {
            "status": "success",
            "message": "ETL pipeline completed",
            "details": result
        }
    except ImportError:
        return {
            "status": "pending",
            "message": "ETL pipeline not yet implemented. Coming in Phase 5."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ETL failed: {str(e)}")


@router.get("/status")
async def etl_status(db: Session = Depends(get_db)):
    """Check the current data status."""
    raw_count = db.query(func.count(RawData.id)).scalar() or 0
    metrics_count = db.query(func.count(CalculatedMetrics.id)).scalar() or 0

    last_load = db.query(func.max(RawData.loaded_at)).scalar()
    last_calc = db.query(func.max(CalculatedMetrics.calculated_at)).scalar()

    return {
        "raw_data_rows": raw_count,
        "calculated_metrics_rows": metrics_count,
        "last_data_load": str(last_load) if last_load else None,
        "last_calculation": str(last_calc) if last_calc else None,
        "status": "ready" if raw_count > 0 else "no_data"
    }