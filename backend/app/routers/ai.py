# backend/app/routers/ai.py
"""
AI Insights & Chat API endpoints.
Connects to Ollama for AI-powered financial analysis.
Falls back to rule-based insights if Ollama is unavailable.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chat import ChatMessageRequest
from app.models.insight import AIInsight
from app.models.chat import ChatHistory
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.ai.insights_engine import generate_all_insights
from app.ai.chat_engine import chat_with_advisor
from app.ai.ollama_client import ollama_client

router = APIRouter()


@router.get("/status")
async def ai_status():
    """Check if AI (Ollama) is available."""
    is_available = await ollama_client.is_available()
    return {
        "ollama_available": is_available,
        "model": ollama_client.model,
        "base_url": ollama_client.base_url,
        "message": "Ollama is running and ready" if is_available else "Ollama is not running. Start it with 'ollama serve'. Rule-based insights will be used as fallback."
    }


@router.get("/insights")
async def get_insights(db: Session = Depends(get_db)):
    """Get AI-generated insights about startup metrics."""
    # Check if we have cached insights
    existing = db.query(AIInsight).order_by(AIInsight.generated_at.desc()).limit(10).all()

    if existing:
        return {
            "insights": [
                {
                    "id": i.id,
                    "insight_type": i.insight_type,
                    "segment": i.segment,
                    "insight_text": i.insight_text,
                    "severity": i.severity,
                    "recommendation": i.recommendation,
                    "metric_value": i.metric_value,
                    "generated_at": str(i.generated_at)
                }
                for i in existing
            ],
            "total": len(existing),
            "source": "cached"
        }

    # No cached insights — generate new ones
    insights = await generate_all_insights(db)

    return {
        "insights": insights,
        "total": len(insights),
        "source": "generated"
    }


@router.post("/insights/generate")
async def regenerate_insights(db: Session = Depends(get_db)):
    """Force regenerate all AI insights."""
    insights = await generate_all_insights(db)
    return {
        "insights": insights,
        "total": len(insights),
        "source": "freshly_generated"
    }


@router.post("/chat")
async def chat_endpoint(
    message: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with the AI financial advisor."""
    response = await chat_with_advisor(
        db=db,
        user_id=current_user.id,
        user_message=message.message
    )

    return {
        "role": "assistant",
        "content": response
    }


@router.get("/chat/history")
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for current user."""
    messages = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id
    ).order_by(ChatHistory.created_at.asc()).limit(50).all()

    return {
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": str(m.created_at)
            }
            for m in messages
        ],
        "total": len(messages)
    }


@router.delete("/chat/history")
async def clear_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear chat history for current user."""
    deleted = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id
    ).delete()
    db.commit()

    return {
        "message": f"Cleared {deleted} messages",
        "status": "success"
    }