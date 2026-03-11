# backend/app/ai/insights_engine.py
"""
AI Insights Engine.
Takes calculated metrics and generates human-readable insights
using the Ollama AI model.
"""

import re
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.ai.ollama_client import ollama_client
from app.ai.prompts import (
    SYSTEM_PROMPT,
    INSIGHTS_PROMPT,
    CAC_ANALYSIS_PROMPT,
    LTV_ANALYSIS_PROMPT,
    BURN_RATE_PROMPT,
    RUNWAY_ANALYSIS_PROMPT,
)
from app.services.metrics_engine import MetricsEngine
from app.services.metrics_service import get_overall_summary
from app.models.insight import AIInsight


# In backend/app/ai/insights_engine.py
# Replace the generate_all_insights function:

# In backend/app/ai/insights_engine.py
# Replace the generate_all_insights function:

async def generate_all_insights(db: Session) -> List[Dict[str, Any]]:
    """
    Generate comprehensive AI insights from all metrics.
    Falls back to rule-based if AI times out.
    """
    print("[AI] Generating insights...")

    # Get all metrics
    summary = get_overall_summary(db)
    engine = MetricsEngine(db)
    channel_metrics = engine.get_cac_by_channel()

    # Check if we have data
    if summary["total_records"] == 0:
        return [{
            "insight_type": "info",
            "segment": "overall",
            "insight_text": "No data loaded yet. Please run the ETL pipeline first.",
            "severity": "warning",
            "recommendation": "Go to the ETL section and click 'Run Pipeline'.",
            "metric_value": "N/A"
        }]

    # Check if Ollama is available
    is_ai_available = await ollama_client.is_available()

    if is_ai_available:
        try:
            # Try AI-powered insights
            insights = await generate_ai_insights(db, summary, channel_metrics)
            
            # Check if AI timed out
            if len(insights) == 1 and "TIMEOUT" in str(insights[0].get("insight_text", "")):
                print("[AI] AI timed out, falling back to rule-based insights")
                insights = generate_rule_based_insights(summary, channel_metrics)
        except Exception as e:
            print(f"[AI] AI failed: {e}, falling back to rule-based")
            insights = generate_rule_based_insights(summary, channel_metrics)
    else:
        print("[AI] Ollama not available. Using rule-based insights.")
        insights = generate_rule_based_insights(summary, channel_metrics)

    # Save insights to database
    save_insights(db, insights)

    return insights


async def generate_ai_insights(
    db: Session,
    summary: Dict[str, Any],
    channel_metrics: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Generate insights using Ollama AI model."""
    print("[AI] Using Ollama for AI-powered insights...")

    # Format channel data for the prompt
    channel_data = ""
    for ch in channel_metrics:
        channel_data += f"  - {ch['channel']}: CAC=${ch['cac']:.2f}, "
        channel_data += f"Conversions={ch['customers_acquired']}, "
        channel_data += f"Spend=${ch['total_ad_spend']:,.2f}\n"

    # Build the prompt
    prompt = INSIGHTS_PROMPT.format(
        total_ad_spend=summary["total_ad_spend"],
        total_conversions=summary["total_conversions"],
        cac=summary["overall_cac"],
        ltv=summary["average_ltv"],
        ltv_cac_ratio=summary["ltv_cac_ratio"],
        burn_rate=summary["estimated_burn_rate"],
        runway=summary["estimated_runway_months"],
        is_profitable="Yes" if summary.get("is_healthy") else "No",
        channel_data=channel_data
    )

    # Get AI response
    response = await ollama_client.generate(prompt, system_prompt=SYSTEM_PROMPT)

    # Parse the AI response into structured insights
    insights = parse_ai_response(response, summary)

    return insights


def parse_ai_response(response: str, summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse AI text response into structured insight objects."""
    insights = []

    # Try to parse numbered insights from AI response
    lines = response.strip().split("\n")
    current_insight = ""
    insight_count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is a new numbered insight
        if re.match(r'^\d+\.', line):
            # Save previous insight if exists
            if current_insight and insight_count > 0:
                parsed = parse_single_insight(current_insight, insight_count)
                if parsed:
                    insights.append(parsed)

            current_insight = line
            insight_count += 1
        else:
            current_insight += " " + line

    # Don't forget the last insight
    if current_insight and insight_count > 0:
        parsed = parse_single_insight(current_insight, insight_count)
        if parsed:
            insights.append(parsed)

    # If parsing failed, create one big insight
    if not insights:
        insights.append({
            "insight_type": "overall",
            "segment": "overall",
            "insight_text": response[:500],
            "severity": determine_overall_severity(summary),
            "recommendation": "Review the detailed metrics for specific action items.",
            "metric_value": f"CAC: ${summary['overall_cac']:.2f}"
        })

    return insights


def parse_single_insight(text: str, index: int) -> Dict[str, Any]:
    """Parse a single insight line into a structured dict."""
    # Remove the number prefix
    text = re.sub(r'^\d+\.\s*', '', text)

    # Try to extract severity
    severity = "warning"
    severity_match = re.search(r'\[(SEVERITY:\s*)?(good|warning|critical)\]', text, re.IGNORECASE)
    if severity_match:
        severity = severity_match.group(2).lower()
        text = re.sub(r'\[.*?\]', '', text, count=1).strip()

    # Try to split into insight and recommendation
    recommendation = ""
    rec_match = re.search(r'RECOMMENDATION:\s*(.*)', text, re.IGNORECASE)
    if rec_match:
        recommendation = rec_match.group(1).strip()
        text = re.sub(r'RECOMMENDATION:.*', '', text, re.IGNORECASE).strip()

    # Determine insight type based on content
    insight_type = "overall"
    text_lower = text.lower()
    if "cac" in text_lower or "acquisition" in text_lower:
        insight_type = "cac"
    elif "ltv" in text_lower or "lifetime" in text_lower:
        insight_type = "ltv"
    elif "burn" in text_lower:
        insight_type = "burn_rate"
    elif "runway" in text_lower:
        insight_type = "runway"
    elif "conversion" in text_lower:
        insight_type = "conversion"
    elif "channel" in text_lower or "roi" in text_lower:
        insight_type = "channel_roi"

    return {
        "insight_type": insight_type,
        "segment": "overall",
        "insight_text": text.strip(),
        "severity": severity,
        "recommendation": recommendation or "Review this metric and take appropriate action.",
        "metric_value": ""
    }


def determine_overall_severity(summary: Dict[str, Any]) -> str:
    """Determine overall health severity from metrics."""
    ratio = summary.get("ltv_cac_ratio", 0)
    runway = summary.get("estimated_runway_months", 0)

    if ratio >= 3 and runway >= 12:
        return "good"
    elif ratio >= 1 and runway >= 6:
        return "warning"
    else:
        return "critical"


def generate_rule_based_insights(
    summary: Dict[str, Any],
    channel_metrics: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate insights using rules when AI is not available.
    This ensures the app always shows insights.
    """
    print("[AI] Generating rule-based insights...")
    insights = []

    cac = summary.get("overall_cac", 0)
    ltv = summary.get("average_ltv", 0)
    ratio = summary.get("ltv_cac_ratio", 0)
    burn = summary.get("estimated_burn_rate", 0)
    runway = summary.get("estimated_runway_months", 0)

    # Insight 1: CAC Analysis
    if cac > 0:
        if cac < 50:
            insights.append({
                "insight_type": "cac",
                "segment": "overall",
                "insight_text": f"Your Customer Acquisition Cost of ${cac:.2f} is excellent. This indicates highly efficient marketing spend. You're acquiring customers at a very competitive rate.",
                "severity": "good",
                "recommendation": "Maintain current acquisition channels and consider scaling ad spend to grow faster.",
                "metric_value": f"${cac:.2f}"
            })
        elif cac < 150:
            insights.append({
                "insight_type": "cac",
                "segment": "overall",
                "insight_text": f"Your CAC of ${cac:.2f} is moderate. While not alarming, there's room for improvement. Consider optimizing your worst-performing channels.",
                "severity": "warning",
                "recommendation": "A/B test ad creatives and landing pages. Focus budget on channels with lowest CAC.",
                "metric_value": f"${cac:.2f}"
            })
        else:
            insights.append({
                "insight_type": "cac",
                "segment": "overall",
                "insight_text": f"Your CAC of ${cac:.2f} is high. You're spending too much to acquire each customer. This is unsustainable long-term and will accelerate cash burn.",
                "severity": "critical",
                "recommendation": "Immediately audit marketing channels. Cut spend on channels with CAC above ${:.2f}. Invest in organic growth channels.".format(cac * 0.7),
                "metric_value": f"${cac:.2f}"
            })

    # Insight 2: LTV Analysis
    if ltv > 0:
        if ltv > cac * 3:
            insights.append({
                "insight_type": "ltv",
                "segment": "overall",
                "insight_text": f"Your LTV of ${ltv:.2f} is {ratio:.1f}x your CAC. This is a strong unit economics position. Each customer generates significantly more revenue than their acquisition cost.",
                "severity": "good",
                "recommendation": "Focus on customer retention to maintain high LTV. Consider loyalty programs and upselling.",
                "metric_value": f"${ltv:.2f}"
            })
        elif ltv > cac:
            insights.append({
                "insight_type": "ltv",
                "segment": "overall",
                "insight_text": f"Your LTV of ${ltv:.2f} is only {ratio:.1f}x your CAC. The industry benchmark is 3x or higher. Your unit economics are thin.",
                "severity": "warning",
                "recommendation": "Increase LTV by improving retention, raising prices, or adding premium features. Target LTV:CAC ratio of 3x.",
                "metric_value": f"${ltv:.2f}"
            })
        else:
            insights.append({
                "insight_type": "ltv",
                "segment": "overall",
                "insight_text": f"CRITICAL: Your LTV of ${ltv:.2f} is BELOW your CAC of ${cac:.2f}. You are losing money on every customer. This is not sustainable.",
                "severity": "critical",
                "recommendation": "This is urgent. Either drastically reduce CAC or find ways to increase customer lifetime value immediately.",
                "metric_value": f"${ltv:.2f}"
            })

    # Insight 3: LTV:CAC Ratio
    if ratio > 0:
        insights.append({
            "insight_type": "ltv_cac_ratio",
            "segment": "overall",
            "insight_text": f"Your LTV:CAC ratio is {ratio:.2f}x. " + (
                "This is above the healthy threshold of 3x. Your business model is working well."
                if ratio >= 3 else
                "This is below the healthy threshold of 3x. You need to either increase LTV or decrease CAC."
                if ratio >= 1 else
                "This is below 1x, meaning you lose money on every customer. Immediate action required."
            ),
            "severity": "good" if ratio >= 3 else "warning" if ratio >= 1 else "critical",
            "recommendation": (
                "Consider investing more in growth since unit economics are healthy."
                if ratio >= 3 else
                "Focus on improving retention and reducing acquisition costs."
                if ratio >= 1 else
                "Pause paid marketing immediately. Focus only on profitable channels."
            ),
            "metric_value": f"{ratio:.2f}x"
        })

    # Insight 4: Burn Rate
    if burn > 0:
        if burn < 50000:
            severity = "good"
            text = f"Your monthly burn rate of ${burn:,.2f} is manageable. You're spending conservatively."
            rec = "Good financial discipline. Make sure you're not under-investing in growth."
        elif burn < 150000:
            severity = "warning"
            text = f"Your monthly burn rate of ${burn:,.2f} is moderate. Monitor closely and ensure revenue growth outpaces expenses."
            rec = "Review all expenses monthly. Cut non-essential costs and focus on ROI-positive spending."
        else:
            severity = "critical"
            text = f"Your monthly burn rate of ${burn:,.2f} is high. At this rate, you'll deplete cash reserves quickly."
            rec = "Implement immediate cost controls. Reduce team size or marketing spend to extend runway."

        insights.append({
            "insight_type": "burn_rate",
            "segment": "overall",
            "insight_text": text,
            "severity": severity,
            "recommendation": rec,
            "metric_value": f"${burn:,.2f}/month"
        })

    # Insight 5: Runway
    if runway > 0:
        if runway >= 18:
            severity = "good"
            text = f"Your estimated runway is {runway:.0f} months. This gives you plenty of time to grow and iterate."
            rec = "Use this time wisely. Focus on product-market fit and scaling revenue."
        elif runway >= 12:
            severity = "good"
            text = f"Your runway of {runway:.0f} months is comfortable but start planning your next fundraise."
            rec = "Begin fundraising preparations now. You should start pitching in 3-4 months."
        elif runway >= 6:
            severity = "warning"
            text = f"Your runway of {runway:.0f} months is getting tight. This is the danger zone for startups."
            rec = "Start fundraising immediately or implement aggressive cost cuts to extend runway to 12+ months."
        else:
            severity = "critical"
            text = f"CRITICAL: Only {runway:.0f} months of runway remaining. Your startup is at immediate risk of running out of cash."
            rec = "Emergency measures needed: Cut all non-essential spending, explore bridge financing, or consider revenue-generating pivots."

        insights.append({
            "insight_type": "runway",
            "segment": "overall",
            "insight_text": text,
            "severity": severity,
            "recommendation": rec,
            "metric_value": f"{runway:.0f} months"
        })

    # Insight 6: Best/Worst Channel
    if channel_metrics:
        sorted_channels = sorted(channel_metrics, key=lambda x: x.get("cac", 999))
        best = sorted_channels[0]
        worst = sorted_channels[-1]

        insights.append({
            "insight_type": "channel_roi",
            "segment": "channels",
            "insight_text": f"Best performing channel: {best['channel']} (CAC: ${best['cac']:.2f}). "
                          f"Worst performing: {worst['channel']} (CAC: ${worst['cac']:.2f}). "
                          f"The difference is ${worst['cac'] - best['cac']:.2f} per customer.",
            "severity": "warning" if worst["cac"] > best["cac"] * 2 else "good",
            "recommendation": f"Shift more budget to {best['channel']} and reduce spend on {worst['channel']}.",
            "metric_value": f"Best: ${best['cac']:.2f}"
        })

    return insights


def save_insights(db: Session, insights: List[Dict[str, Any]]) -> None:
    """Save generated insights to the database."""
    try:
        # Clear old insights
        db.query(AIInsight).delete()
        db.commit()

        # Save new insights
        for insight_data in insights:
            insight = AIInsight(
                insight_type=insight_data["insight_type"],
                segment=insight_data.get("segment", "overall"),
                insight_text=insight_data["insight_text"],
                severity=insight_data["severity"],
                recommendation=insight_data.get("recommendation", ""),
                metric_value=insight_data.get("metric_value", "")
            )
            db.add(insight)

        db.commit()
        print(f"[AI] Saved {len(insights)} insights to database.")
    except Exception as e:
        print(f"[AI] Error saving insights: {e}")
        db.rollback()