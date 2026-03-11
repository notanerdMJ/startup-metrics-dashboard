# backend/app/etl/load.py
"""
LOAD phase of the ETL pipeline.
Inserts cleaned data and calculated metrics into PostgreSQL.
"""

import pandas as pd
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.models.raw_data import RawData
from app.models.metrics import CalculatedMetrics


def load_raw_data(db: Session, df: pd.DataFrame) -> dict:
    """
    Load cleaned raw data into the raw_data table.
    Clears existing data first to avoid duplicates.
    """
    print("[LOAD] Loading raw data into database...")

    # Clear existing raw data
    deleted_count = db.query(RawData).delete()
    db.commit()
    print(f"  Cleared {deleted_count} existing raw data rows")

    # Convert DataFrame rows to RawData model objects
    records = []
    for _, row in df.iterrows():
        record = RawData(
            customerid=safe_int(row.get("customerid")),
            age=safe_int(row.get("age")),
            gender=safe_str(row.get("gender")),
            income=safe_float(row.get("income")),
            campaignchannel=safe_str(row.get("campaignchannel")),
            campaigntype=safe_str(row.get("campaigntype")),
            adspend=safe_float(row.get("adspend")),
            clickthroughrate=safe_float(row.get("clickthroughrate")),
            conversionrate=safe_float(row.get("conversionrate")),
            websitevisits=safe_int(row.get("websitevisits")),
            pagespervisit=safe_float(row.get("pagespervisit")),
            timeonsite=safe_float(row.get("timeonsite")),
            socialshares=safe_int(row.get("socialshares")),
            emailopens=safe_int(row.get("emailopens")),
            emailclicks=safe_int(row.get("emailclicks")),
            previouspurchases=safe_int(row.get("previouspurchases")),
            loyaltypoints=safe_int(row.get("loyaltypoints")),
            advertisingplatform=safe_str(row.get("advertisingplatform")),
            advertisingtool=safe_str(row.get("advertisingtool")),
            conversion=safe_int(row.get("conversion")),
            channel_used=safe_str(row.get("channel_used")),
            social_agg_conversion_rate=safe_float(row.get("social_agg_conversion_rate")),
            social_agg_acquisition_cost=safe_float(row.get("social_agg_acquisition_cost")),
        )
        records.append(record)

    # Batch insert (much faster than one-by-one)
    BATCH_SIZE = 1000
    total_inserted = 0

    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        db.bulk_save_objects(batch)
        db.commit()
        total_inserted += len(batch)
        print(f"  Inserted batch {i // BATCH_SIZE + 1}: {total_inserted}/{len(records)} rows")

    stats = {
        "rows_inserted": total_inserted,
        "rows_cleared": deleted_count
    }

    print(f"[LOAD] ✅ Raw data loaded. {total_inserted} rows inserted.")
    return stats


def load_metrics(db: Session, metrics_list: List[Dict[str, Any]]) -> dict:
    """
    Load calculated metrics into the calculated_metrics table.
    Clears existing metrics first.
    """
    print("[LOAD] Loading calculated metrics into database...")

    # Clear existing metrics
    deleted_count = db.query(CalculatedMetrics).delete()
    db.commit()
    print(f"  Cleared {deleted_count} existing metric rows")

    # Insert each metric record
    records_inserted = 0
    for metric_data in metrics_list:
        metric = CalculatedMetrics(
            segment_type=metric_data["segment_type"],
            segment_value=metric_data["segment_value"],
            total_ad_spend=metric_data["total_ad_spend"],
            total_customers=metric_data["total_customers"],
            total_conversions=metric_data["total_conversions"],
            cac=metric_data["cac"],
            estimated_ltv=metric_data["estimated_ltv"],
            ltv_cac_ratio=metric_data["ltv_cac_ratio"],
            estimated_revenue=metric_data["estimated_revenue"],
            total_expenses=metric_data["total_expenses"],
            profit_loss=metric_data["profit_loss"],
            is_profitable=metric_data["is_profitable"],
            burn_rate=metric_data["burn_rate"],
            estimated_runway_months=metric_data["estimated_runway_months"],
            avg_conversion_rate=metric_data["avg_conversion_rate"],
            avg_click_through_rate=metric_data["avg_click_through_rate"],
            cost_per_click=metric_data["cost_per_click"],
            avg_income=metric_data["avg_income"],
            avg_previous_purchases=metric_data["avg_previous_purchases"],
            avg_loyalty_points=metric_data["avg_loyalty_points"],
            avg_website_visits=metric_data["avg_website_visits"],
            avg_time_on_site=metric_data["avg_time_on_site"],
        )
        db.add(metric)
        records_inserted += 1

    db.commit()

    stats = {
        "metrics_inserted": records_inserted,
        "metrics_cleared": deleted_count
    }

    print(f"[LOAD] ✅ Metrics loaded. {records_inserted} metric records inserted.")
    return stats


# === Helper Functions ===

def safe_float(value) -> float:
    """Safely convert a value to float."""
    try:
        if pd.isna(value):
            return 0.0
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def safe_int(value) -> int:
    """Safely convert a value to int."""
    try:
        if pd.isna(value):
            return 0
        return int(float(value))
    except (ValueError, TypeError):
        return 0


def safe_str(value) -> str:
    """Safely convert a value to string."""
    try:
        if pd.isna(value):
            return "Unknown"
        return str(value).strip()
    except (ValueError, TypeError):
        return "Unknown"