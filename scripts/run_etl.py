# scripts/run_etl.py
"""
Manual ETL runner script.
Run this to load your dataset into the database.

Usage:
    cd backend
    python ../scripts/run_etl.py
"""

import sys
import os

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal
from app.etl.pipeline import run_pipeline
import json


def main():
    print("🚀 Starting ETL Pipeline...")
    print()

    # Create database session
    db = SessionLocal()

    try:
        # Run the pipeline
        results = run_pipeline(db)

        # Print results
        print("\n" + "=" * 60)
        print("  PIPELINE RESULTS")
        print("=" * 60)
        print(json.dumps(results, indent=2, default=str))

        if results["status"] == "success":
            print("\n✅ SUCCESS! Your data is now in the database.")
            print("   Visit http://localhost:8000/api/v1/metrics/summary to see metrics.")
        else:
            print(f"\n❌ FAILED: {results.get('error', 'Unknown error')}")

    finally:
        db.close()


if __name__ == "__main__":
    main()