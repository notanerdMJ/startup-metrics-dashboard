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
    """Load cleaned raw data into the raw_data table."""
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

    # Batch insert
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
    """Load calculated metrics into the calculated_metrics table."""
    print("[LOAD] Loading calculated metrics into database...")

    # Clear existing metrics
    deleted_count = db.query(CalculatedMetrics).delete()
    db.commit()
    print(f"  Cleared {deleted_count} existing metric rows")

    # Insert each metric record
    records_inserted = 0
    for metric_data in metrics_list:
        try:
            metric = CalculatedMetrics(
                segment_type=str(metric_data.get("segment_type", "unknown")),
                segment_value=str(metric_data.get("segment_value", "unknown")),
                total_ad_spend=to_float(metric_data.get("total_ad_spend", 0)),
                total_customers=to_int(metric_data.get("total_customers", 0)),
                total_conversions=to_int(metric_data.get("total_conversions", 0)),
                cac=to_float(metric_data.get("cac", 0)),
                estimated_ltv=to_float(metric_data.get("estimated_ltv", 0)),
                ltv_cac_ratio=to_float(metric_data.get("ltv_cac_ratio", 0)),
                estimated_revenue=to_float(metric_data.get("estimated_revenue", 0)),
                total_expenses=to_float(metric_data.get("total_expenses", 0)),
                profit_loss=to_float(metric_data.get("profit_loss", 0)),
                is_profitable=bool(metric_data.get("is_profitable", False)),
                burn_rate=to_float(metric_data.get("burn_rate", 0)),
                estimated_runway_months=to_float(metric_data.get("estimated_runway_months", 0)),
                avg_conversion_rate=to_float(metric_data.get("avg_conversion_rate", 0)),
                avg_click_through_rate=to_float(metric_data.get("avg_click_through_rate", 0)),
                cost_per_click=to_float(metric_data.get("cost_per_click", 0)),
                avg_income=to_float(metric_data.get("avg_income", 0)),
                avg_previous_purchases=to_float(metric_data.get("avg_previous_purchases", 0)),
                avg_loyalty_points=to_float(metric_data.get("avg_loyalty_points", 0)),
                avg_website_visits=to_float(metric_data.get("avg_website_visits", 0)),
                avg_time_on_site=to_float(metric_data.get("avg_time_on_site", 0)),
            )
            db.add(metric)
            records_inserted += 1
        except Exception as e:
            print(f"  Warning: Skipped metric {metric_data.get('segment_type')}:{metric_data.get('segment_value')} - {e}")
            continue

    db.commit()

    stats = {
        "metrics_inserted": records_inserted,
        "metrics_cleared": deleted_count
    }

    print(f"[LOAD] ✅ Metrics loaded. {records_inserted} metric records inserted.")
    return stats


# === Helper Functions ===

def to_float(value) -> float:
    """Convert any value to Python float."""
    try:
        if value is None:
            return 0.0
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def to_int(value) -> int:
    """Convert any value to Python int."""
    try:
        if value is None:
            return 0
        return int(float(value))
    except (ValueError, TypeError):
        return 0


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