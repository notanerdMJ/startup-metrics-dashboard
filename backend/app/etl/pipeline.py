# backend/app/etl/pipeline.py
"""
ETL Pipeline Orchestrator.
Runs Extract → Transform → Load in sequence.
Tracks timing and returns comprehensive results.
"""

import time
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.etl.extract import extract_data
from app.etl.transform import transform_data
from app.etl.load import load_raw_data, load_metrics


def run_pipeline(db: Session) -> Dict[str, Any]:
    """
    Execute the complete ETL pipeline.
    
    Steps:
        1. Extract: Read CSV file
        2. Transform: Clean data + calculate metrics
        3. Load: Insert into PostgreSQL
    
    Args:
        db: SQLAlchemy database session
    
    Returns:
        Dictionary with results from each phase
    """
    pipeline_start = time.time()
    results = {
        "status": "running",
        "phases": {}
    }

    try:
        # ===== PHASE 1: EXTRACT =====
        print("\n" + "=" * 60)
        print("  PHASE 1: EXTRACT")
        print("=" * 60)
        extract_start = time.time()

        df, extract_stats = extract_data()

        extract_time = round(time.time() - extract_start, 2)
        results["phases"]["extract"] = {
            "status": "success",
            "duration_seconds": extract_time,
            "stats": extract_stats
        }

        # ===== PHASE 2: TRANSFORM =====
        print("\n" + "=" * 60)
        print("  PHASE 2: TRANSFORM")
        print("=" * 60)
        transform_start = time.time()

        df_clean, metrics_list, transform_stats = transform_data(df)

        transform_time = round(time.time() - transform_start, 2)
        results["phases"]["transform"] = {
            "status": "success",
            "duration_seconds": transform_time,
            "stats": transform_stats
        }

        # ===== PHASE 3: LOAD =====
        print("\n" + "=" * 60)
        print("  PHASE 3: LOAD")
        print("=" * 60)
        load_start = time.time()

        raw_load_stats = load_raw_data(db, df_clean)
        metrics_load_stats = load_metrics(db, metrics_list)

        load_time = round(time.time() - load_start, 2)
        results["phases"]["load"] = {
            "status": "success",
            "duration_seconds": load_time,
            "raw_data": raw_load_stats,
            "metrics": metrics_load_stats
        }

        # ===== PIPELINE COMPLETE =====
        total_time = round(time.time() - pipeline_start, 2)
        results["status"] = "success"
        results["total_duration_seconds"] = total_time
        results["summary"] = {
            "rows_processed": extract_stats["total_rows"],
            "rows_loaded": raw_load_stats["rows_inserted"],
            "metrics_generated": metrics_load_stats["metrics_inserted"],
            "total_time": f"{total_time}s"
        }

        print("\n" + "=" * 60)
        print("  ✅ ETL PIPELINE COMPLETE")
        print(f"  Total time: {total_time}s")
        print(f"  Rows loaded: {raw_load_stats['rows_inserted']}")
        print(f"  Metrics generated: {metrics_load_stats['metrics_inserted']}")
        print("=" * 60)

    except FileNotFoundError as e:
        results["status"] = "error"
        results["error"] = str(e)
        results["error_type"] = "file_not_found"
        print(f"\n❌ ETL FAILED: {e}")

    except Exception as e:
        results["status"] = "error"
        results["error"] = str(e)
        results["error_type"] = type(e).__name__
        print(f"\n❌ ETL FAILED: {e}")
        # Rollback any partial database changes
        db.rollback()

    return results