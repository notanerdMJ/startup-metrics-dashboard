# backend/app/ai/chat_engine.py
"""
AI Chat Engine.
Powers the AI Advisor chat interface.
Uses Ollama for conversations with startup founders.
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.ai.ollama_client import ollama_client
from app.ai.prompts import CHAT_SYSTEM_PROMPT
from app.services.metrics_service import get_overall_summary
from app.services.metrics_engine import MetricsEngine
from app.models.chat import ChatHistory


# In backend/app/ai/chat_engine.py
# Replace the chat_with_advisor function:

# In backend/app/ai/chat_engine.py
# Replace the chat_with_advisor function:

async def chat_with_advisor(
    db: Session,
    user_id: int,
    user_message: str
) -> str:
    """
    Process a chat message and generate AI response.
    """
    print(f"[CHAT] User {user_id}: {user_message[:50]}...")

    # Get current metrics for context
    metrics_context = build_metrics_context(db)

    # Build system prompt with metrics (keep it short)
    system_prompt = f"""You are a startup financial advisor. Answer briefly and clearly.
    
Current metrics:
{metrics_context[:800]}

Give specific advice based on these numbers. Be concise."""

    # Get recent chat history for context
    recent_messages = get_recent_messages(db, user_id, limit=4)

    # Add current user message
    recent_messages.append({
        "role": "user",
        "content": user_message
    })

    # Check if Ollama is available
    is_available = await ollama_client.is_available()

    if is_available:
        # Use AI model
        response = await ollama_client.chat(
            messages=recent_messages,
            system_prompt=system_prompt
        )
        
        # If timeout, use fallback
        if response == "TIMEOUT":
            print("[CHAT] AI timed out, using fallback")
            response = generate_fallback_response(user_message, metrics_context)
    else:
        # Fallback to rule-based response
        response = generate_fallback_response(user_message, metrics_context)

    # Save both messages to database
    save_message(db, user_id, "user", user_message)
    save_message(db, user_id, "assistant", response)

    return response


def build_metrics_context(db: Session) -> str:
    """Build a text summary of current metrics for the AI."""
    try:
        summary = get_overall_summary(db)
        engine = MetricsEngine(db)
        channels = engine.get_cac_by_channel()

        context = f"""
- Total Records: {summary.get('total_records', 0):,}
- Total Ad Spend: ${summary.get('total_ad_spend', 0):,.2f}
- Total Conversions: {summary.get('total_conversions', 0):,}
- CAC (Customer Acquisition Cost): ${summary.get('overall_cac', 0):,.2f}
- LTV (Lifetime Value): ${summary.get('average_ltv', 0):,.2f}
- LTV:CAC Ratio: {summary.get('ltv_cac_ratio', 0):.2f}x
- Monthly Burn Rate: ${summary.get('estimated_burn_rate', 0):,.2f}
- Estimated Runway: {summary.get('estimated_runway_months', 0):.0f} months
- Is Healthy: {'Yes' if summary.get('is_healthy') else 'No'}

Top Channels by CAC:
"""
        for ch in channels[:5]:
            context += f"  - {ch['channel']}: CAC=${ch['cac']:.2f}, Conversions={ch['customers_acquired']}\n"

        return context

    except Exception as e:
        return f"Metrics not available: {str(e)}"


def get_recent_messages(db: Session, user_id: int, limit: int = 6) -> List[Dict[str, str]]:
    """Get recent chat messages for conversation context."""
    messages = db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).order_by(
        ChatHistory.created_at.desc()
    ).limit(limit).all()

    # Reverse to get chronological order
    messages.reverse()

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def save_message(db: Session, user_id: int, role: str, content: str) -> None:
    """Save a chat message to the database."""
    try:
        msg = ChatHistory(
            user_id=user_id,
            role=role,
            content=content
        )
        db.add(msg)
        db.commit()
    except Exception as e:
        print(f"[CHAT] Error saving message: {e}")
        db.rollback()


def generate_fallback_response(user_message: str, metrics_context: str) -> str:
    """Generate a response without AI when Ollama is not available."""
    message_lower = user_message.lower()

    if "cac" in message_lower or "acquisition cost" in message_lower:
        return (
            "Based on your current data, here's what I can tell you about CAC:\n\n"
            f"{metrics_context}\n\n"
            "A healthy CAC depends on your industry, but generally:\n"
            "- CAC under $50 = Excellent\n"
            "- CAC $50-$150 = Moderate\n"
            "- CAC over $150 = Needs optimization\n\n"
            "Recommendation: Focus on your best-performing channels and reduce spend on underperforming ones.\n\n"
            "Note: For more detailed AI analysis, please ensure Ollama is running (run 'ollama serve' in terminal)."
        )

    elif "ltv" in message_lower or "lifetime value" in message_lower:
        return (
            "Here's your LTV analysis:\n\n"
            f"{metrics_context}\n\n"
            "Key LTV benchmarks:\n"
            "- LTV:CAC ratio above 3x = Healthy business model\n"
            "- LTV:CAC ratio 1-3x = Needs improvement\n"
            "- LTV:CAC ratio below 1x = Losing money per customer\n\n"
            "To increase LTV: Improve retention, add premium features, and focus on high-value customer segments."
        )

    elif "burn" in message_lower:
        return (
            "Here's your burn rate analysis:\n\n"
            f"{metrics_context}\n\n"
            "Burn rate tips:\n"
            "- Keep burn rate low enough for 12+ months runway\n"
            "- Monitor monthly and compare against revenue growth\n"
            "- Cut non-essential expenses first\n\n"
            "Recommendation: Review all recurring expenses and eliminate anything not directly driving growth."
        )

    elif "runway" in message_lower:
        return (
            "Here's your runway analysis:\n\n"
            f"{metrics_context}\n\n"
            "Runway guidelines:\n"
            "- 18+ months = Comfortable\n"
            "- 12-18 months = Start fundraising\n"
            "- 6-12 months = Urgent - fundraise now\n"
            "- Under 6 months = Emergency measures needed\n\n"
            "Recommendation: If runway is under 12 months, start fundraising or implement cost cuts immediately."
        )

    else:
        return (
            "Here are your current startup metrics:\n\n"
            f"{metrics_context}\n\n"
            "You can ask me about:\n"
            "- CAC (Customer Acquisition Cost)\n"
            "- LTV (Lifetime Value)\n"
            "- Burn Rate\n"
            "- Runway\n"
            "- Channel performance\n"
            "- How to improve specific metrics\n\n"
            "Note: For detailed AI-powered analysis, please ensure Ollama is running."
        )