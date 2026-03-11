# backend/app/main.py
"""
FastAPI application entry point.
All routers are registered here.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base

# Import all models
from app.models import User, RawData, CalculatedMetrics, AIInsight, ChatHistory

# Import all routers
from app.routers import auth, metrics, dashboard, ai, etl

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Unit Economics & Runway Dashboard for Startups",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Metrics"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI Insights"])
app.include_router(etl.router, prefix="/api/v1/etl", tags=["ETL Pipeline"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0"
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Startup Unit Economics Dashboard API",
        "docs": "/docs",
        "health": "/health"
    }