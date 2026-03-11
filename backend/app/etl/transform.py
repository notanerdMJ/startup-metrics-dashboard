# backend/app/etl/transform.py
"""
TRANSFORM phase of the ETL pipeline.
Cleans the raw data and calculates all unit economics metrics:
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)
- Burn Rate
- Runway
- Profitability analysis
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any


def transform_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict[str, Any]], dict]:
    """
    Clean the data and calculate all metrics.
    
    Args:
        df: Raw DataFrame from extract phase
    
    Returns:
        Tuple of (cleaned_df, metrics_list, transform_stats)
    """
    print("[TRANSFORM] Starting data transformation...")

    # ===== STEP 1: Clean the data =====
    df_clean = clean_data(df)

    # ===== STEP 2: Calculate overall metrics =====
    overall_metrics = calculate_overall_metrics(df_clean)

    # ===== STEP 3: Calculate channel-wise metrics =====
    channel_metrics = calculate_channel_metrics(df_clean)

    # ===== STEP 4: Calculate campaign type metrics =====
    campaign_metrics = calculate_campaign_metrics(df_clean)

    # ===== STEP 5: Calculate age group metrics =====
    age_metrics = calculate_age_group_metrics(df_clean)

    # ===== STEP 6: Calculate platform metrics =====
    platform_metrics = calculate_platform_metrics(df_clean)

    # Combine all metrics
    all_metrics = [overall_metrics] + channel_metrics + campaign_metrics + age_metrics + platform_metrics

    # Transform stats
    stats = {
        "rows_before_cleaning": len(df),
        "rows_after_cleaning": len(df_clean),
        "rows_removed": len(df) - len(df_clean),
        "total_metrics_calculated": len(all_metrics),
        "segments": {
            "overall": 1,
            "channels": len(channel_metrics),
            "campaigns": len(campaign_metrics),
            "age_groups": len(age_metrics),
            "platforms": len(platform_metrics),
        }
    }

    print(f"[TRANSFORM] ✅ Transformation complete. {len(all_metrics)} metric records generated.")
    return df_clean, all_metrics, stats


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw DataFrame.
    - Remove duplicates
    - Handle missing values
    - Fix data types
    - Remove invalid records
    """
    print("[TRANSFORM] Cleaning data...")
    df_clean = df.copy()

    # Remove exact duplicate rows
    initial_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    dupes_removed = initial_count - len(df_clean)
    print(f"  Duplicates removed: {dupes_removed}")

    # Fill missing numeric values with median
    numeric_cols = [
        "age", "income", "adspend", "clickthroughrate", "conversionrate",
        "websitevisits", "pagespervisit", "timeonsite", "socialshares",
        "emailopens", "emailclicks", "previouspurchases", "loyaltypoints",
        "social_agg_conversion_rate", "social_agg_acquisition_cost"
    ]

    for col in numeric_cols:
        if col in df_clean.columns:
            null_count = df_clean[col].isnull().sum()
            if null_count > 0:
                median_val = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(median_val)
                print(f"  Filled {null_count} nulls in '{col}' with median {median_val:.2f}")

    # Fill missing categorical values with 'Unknown'
    cat_cols = ["gender", "campaignchannel", "campaigntype", 
                "advertisingplatform", "advertisingtool", "channel_used"]
    
    for col in cat_cols:
        if col in df_clean.columns:
            null_count = df_clean[col].isnull().sum()
            if null_count > 0:
                df_clean[col] = df_clean[col].fillna("Unknown")
                print(f"  Filled {null_count} nulls in '{col}' with 'Unknown'")

    # Ensure conversion is 0 or 1
    if "conversion" in df_clean.columns:
        df_clean["conversion"] = df_clean["conversion"].astype(int).clip(0, 1)

    # Remove rows where adspend is negative
    if "adspend" in df_clean.columns:
        neg_spend = (df_clean["adspend"] < 0).sum()
        if neg_spend > 0:
            df_clean = df_clean[df_clean["adspend"] >= 0]
            print(f"  Removed {neg_spend} rows with negative ad spend")

    print(f"  Final clean dataset: {len(df_clean)} rows")
    return df_clean


def calculate_overall_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate overall metrics across the entire dataset."""
    print("[TRANSFORM] Calculating overall metrics...")

    total_ad_spend = df["adspend"].sum() if "adspend" in df.columns else 0
    total_conversions = df["conversion"].sum() if "conversion" in df.columns else 0
    total_customers = len(df)
    avg_income = df["income"].mean() if "income" in df.columns else 0
    avg_purchases = df["previouspurchases"].mean() if "previouspurchases" in df.columns else 0
    avg_loyalty = df["loyaltypoints"].mean() if "loyaltypoints" in df.columns else 0
    avg_conv_rate = df["conversionrate"].mean() if "conversionrate" in df.columns else 0
    avg_ctr = df["clickthroughrate"].mean() if "clickthroughrate" in df.columns else 0
    avg_visits = df["websitevisits"].mean() if "websitevisits" in df.columns else 0
    avg_time = df["timeonsite"].mean() if "timeonsite" in df.columns else 0

    # CAC = Total Ad Spend / Total Conversions
    cac = total_ad_spend / total_conversions if total_conversions > 0 else 0

    # LTV = Average Income × Purchase Frequency Factor × Retention Factor
    purchase_factor = avg_purchases * 0.15 if avg_purchases > 0 else 1
    retention_factor = 1 + (avg_loyalty / 1000) if avg_loyalty > 0 else 1
    ltv = avg_income * purchase_factor * retention_factor * 0.01

    # LTV:CAC Ratio
    ltv_cac_ratio = ltv / cac if cac > 0 else 0

    # Estimated Revenue (from conversions × estimated revenue per conversion)
    revenue_per_conversion = avg_income * 0.05  # 5% of income as revenue proxy
    estimated_revenue = total_conversions * revenue_per_conversion

    # Burn Rate = Total Expenses (ad spend) - Revenue per month
    monthly_ad_spend = total_ad_spend / 12
    monthly_revenue = estimated_revenue / 12
    burn_rate = monthly_ad_spend - monthly_revenue

    # Profit/Loss
    profit_loss = estimated_revenue - total_ad_spend
    is_profitable = profit_loss > 0

    # Runway (assuming $1M bank balance)
    simulated_bank_balance = 1000000
    runway_months = simulated_bank_balance / burn_rate if burn_rate > 0 else 999

    # Cost per click
    total_clicks = (df["websitevisits"] * df["clickthroughrate"]).sum() if "websitevisits" in df.columns and "clickthroughrate" in df.columns else 0
    cost_per_click = total_ad_spend / total_clicks if total_clicks > 0 else 0

    metrics = {
        "segment_type": "overall",
        "segment_value": "all",
        "total_ad_spend": round(total_ad_spend, 2),
        "total_customers": total_customers,
        "total_conversions": int(total_conversions),
        "cac": round(cac, 2),
        "estimated_ltv": round(ltv, 2),
        "ltv_cac_ratio": round(ltv_cac_ratio, 2),
        "estimated_revenue": round(estimated_revenue, 2),
        "total_expenses": round(total_ad_spend, 2),
        "profit_loss": round(profit_loss, 2),
        "is_profitable": is_profitable,
        "burn_rate": round(burn_rate, 2),
        "estimated_runway_months": round(min(runway_months, 999), 1),
        "avg_conversion_rate": round(avg_conv_rate, 4),
        "avg_click_through_rate": round(avg_ctr, 4),
        "cost_per_click": round(cost_per_click, 2),
        "avg_income": round(avg_income, 2),
        "avg_previous_purchases": round(avg_purchases, 2),
        "avg_loyalty_points": round(avg_loyalty, 2),
        "avg_website_visits": round(avg_visits, 2),
        "avg_time_on_site": round(avg_time, 2),
    }

    print(f"  Overall CAC: ${cac:.2f}")
    print(f"  Overall LTV: ${ltv:.2f}")
    print(f"  LTV:CAC Ratio: {ltv_cac_ratio:.2f}")
    print(f"  Monthly Burn Rate: ${burn_rate:.2f}")
    print(f"  Runway: {runway_months:.1f} months")

    return metrics


def calculate_segment_metrics(df_segment: pd.DataFrame, segment_type: str, segment_value: str) -> Dict[str, Any]:
    """Calculate metrics for a specific segment (channel, campaign, etc.)."""
    
    total_ad_spend = df_segment["adspend"].sum() if "adspend" in df_segment.columns else 0
    total_conversions = df_segment["conversion"].sum() if "conversion" in df_segment.columns else 0
    total_customers = len(df_segment)
    avg_income = df_segment["income"].mean() if "income" in df_segment.columns else 0
    avg_purchases = df_segment["previouspurchases"].mean() if "previouspurchases" in df_segment.columns else 0
    avg_loyalty = df_segment["loyaltypoints"].mean() if "loyaltypoints" in df_segment.columns else 0
    avg_conv_rate = df_segment["conversionrate"].mean() if "conversionrate" in df_segment.columns else 0
    avg_ctr = df_segment["clickthroughrate"].mean() if "clickthroughrate" in df_segment.columns else 0
    avg_visits = df_segment["websitevisits"].mean() if "websitevisits" in df_segment.columns else 0
    avg_time = df_segment["timeonsite"].mean() if "timeonsite" in df_segment.columns else 0

    cac = total_ad_spend / total_conversions if total_conversions > 0 else 0

    purchase_factor = avg_purchases * 0.15 if avg_purchases > 0 else 1
    retention_factor = 1 + (avg_loyalty / 1000) if avg_loyalty > 0 else 1
    ltv = avg_income * purchase_factor * retention_factor * 0.01

    ltv_cac_ratio = ltv / cac if cac > 0 else 0

    revenue_per_conversion = avg_income * 0.05
    estimated_revenue = total_conversions * revenue_per_conversion
    profit_loss = estimated_revenue - total_ad_spend
    is_profitable = profit_loss > 0

    monthly_spend = total_ad_spend / 12
    monthly_rev = estimated_revenue / 12
    burn_rate = monthly_spend - monthly_rev

    simulated_bank = 1000000
    runway = simulated_bank / burn_rate if burn_rate > 0 else 999

    total_clicks = (df_segment["websitevisits"] * df_segment["clickthroughrate"]).sum() if "websitevisits" in df_segment.columns and "clickthroughrate" in df_segment.columns else 0
    cost_per_click = total_ad_spend / total_clicks if total_clicks > 0 else 0

    return {
        "segment_type": segment_type,
        "segment_value": segment_value,
        "total_ad_spend": round(total_ad_spend, 2),
        "total_customers": total_customers,
        "total_conversions": int(total_conversions),
        "cac": round(cac, 2),
        "estimated_ltv": round(ltv, 2),
        "ltv_cac_ratio": round(ltv_cac_ratio, 2),
        "estimated_revenue": round(estimated_revenue, 2),
        "total_expenses": round(total_ad_spend, 2),
        "profit_loss": round(profit_loss, 2),
        "is_profitable": is_profitable,
        "burn_rate": round(burn_rate, 2),
        "estimated_runway_months": round(min(runway, 999), 1),
        "avg_conversion_rate": round(avg_conv_rate, 4),
        "avg_click_through_rate": round(avg_ctr, 4),
        "cost_per_click": round(cost_per_click, 2),
        "avg_income": round(avg_income, 2),
        "avg_previous_purchases": round(avg_purchases, 2),
        "avg_loyalty_points": round(avg_loyalty, 2),
        "avg_website_visits": round(avg_visits, 2),
        "avg_time_on_site": round(avg_time, 2),
    }


def calculate_channel_metrics(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Calculate metrics for each campaign channel."""
    print("[TRANSFORM] Calculating channel metrics...")
    
    if "campaignchannel" not in df.columns:
        return []

    metrics = []
    for channel in df["campaignchannel"].unique():
        df_channel = df[df["campaignchannel"] == channel]
        channel_metrics = calculate_segment_metrics(df_channel, "channel", str(channel))
        metrics.append(channel_metrics)
        print(f"  Channel '{channel}': CAC=${channel_metrics['cac']:.2f}, LTV=${channel_metrics['estimated_ltv']:.2f}")

    return metrics


def calculate_campaign_metrics(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Calculate metrics for each campaign type."""
    print("[TRANSFORM] Calculating campaign type metrics...")
    
    if "campaigntype" not in df.columns:
        return []

    metrics = []
    for campaign in df["campaigntype"].unique():
        df_campaign = df[df["campaigntype"] == campaign]
        campaign_metrics = calculate_segment_metrics(df_campaign, "campaign", str(campaign))
        metrics.append(campaign_metrics)
        print(f"  Campaign '{campaign}': CAC=${campaign_metrics['cac']:.2f}")

    return metrics


def calculate_age_group_metrics(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Calculate metrics for age groups."""
    print("[TRANSFORM] Calculating age group metrics...")
    
    if "age" not in df.columns:
        return []

    # Create age groups
    df_copy = df.copy()
    bins = [0, 25, 35, 45, 55, 100]
    labels = ["18-25", "26-35", "36-45", "46-55", "55+"]
    df_copy["age_group"] = pd.cut(df_copy["age"], bins=bins, labels=labels, right=True)

    metrics = []
    for group in labels:
        df_group = df_copy[df_copy["age_group"] == group]
        if len(df_group) > 0:
            group_metrics = calculate_segment_metrics(df_group, "age_group", group)
            metrics.append(group_metrics)
            print(f"  Age '{group}': CAC=${group_metrics['cac']:.2f}, Customers={group_metrics['total_customers']}")

    return metrics


def calculate_platform_metrics(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Calculate metrics for each advertising platform."""
    print("[TRANSFORM] Calculating platform metrics...")
    
    if "advertisingplatform" not in df.columns:
        return []

    metrics = []
    for platform in df["advertisingplatform"].unique():
        df_platform = df[df["advertisingplatform"] == platform]
        platform_metrics = calculate_segment_metrics(df_platform, "platform", str(platform))
        metrics.append(platform_metrics)
        print(f"  Platform '{platform}': CAC=${platform_metrics['cac']:.2f}")

    return metrics