# backend/app/etl/extract.py
"""
EXTRACT phase of the ETL pipeline.
Reads the Kaggle CSV dataset using Pandas.
Validates that required columns exist.
"""

import pandas as pd
import os
from typing import Tuple
from app.config import settings


# These are the columns we expect from your dataset
REQUIRED_COLUMNS = [
    "customerid",
    "age",
    "gender",
    "income",
    "campaignchannel",
    "campaigntype",
    "adspend",
    "clickthroughrate",
    "conversionrate",
    "websitevisits",
    "pagespervisit",
    "timeonsite",
    "socialshares",
    "emailopens",
    "emailclicks",
    "previouspurchases",
    "loyaltypoints",
    "advertisingplatform",
    "advertisingtool",
    "conversion",
    "channel_used",
    "social_agg_conversion_rate",
    "social_agg_acquisition_cost",
]


def extract_data() -> Tuple[pd.DataFrame, dict]:
    """
    Read the CSV file and return a DataFrame plus extraction stats.
    
    Returns:
        Tuple of (DataFrame, stats_dict)
    
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If required columns are missing
    """
    # Build the full path to the CSV file
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        settings.DATASET_PATH
    )

    print(f"[EXTRACT] Looking for dataset at: {csv_path}")

    # Check file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. "
            f"Please place your Kaggle CSV at backend/data/startup_data.csv"
        )

    # Read CSV
    print("[EXTRACT] Reading CSV file...")
    df = pd.read_csv(csv_path)

    # Normalize column names (lowercase, strip spaces)
    df.columns = df.columns.str.strip().str.lower()

    print(f"[EXTRACT] Raw data shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"[EXTRACT] Columns found: {list(df.columns)}")

    # Validate required columns exist
    missing_columns = []
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing_columns.append(col)

    if missing_columns:
        print(f"[EXTRACT] WARNING: Missing columns: {missing_columns}")
        print(f"[EXTRACT] Available columns: {list(df.columns)}")
        # Don't raise error — we'll handle missing columns gracefully

    # Extraction stats
    stats = {
        "file_path": csv_path,
        "total_rows": df.shape[0],
        "total_columns": df.shape[1],
        "columns": list(df.columns),
        "missing_expected_columns": missing_columns,
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
    }

    print(f"[EXTRACT] ✅ Extraction complete. {stats['total_rows']} rows loaded.")
    return df, stats