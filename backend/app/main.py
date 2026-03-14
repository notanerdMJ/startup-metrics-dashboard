# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
import traceback

app = FastAPI(
    title=settings.APP_NAME,
    description="Unit Economics & Runway Dashboard for Startups",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS — Allow ALL origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://startup-metrics-dashboard-bsj1.vercel.app",
        "https://startup-metrics-dashboard-bsj1-git-main-notanerdmjs-projects.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_detail = traceback.format_exc()
    print(f"ERROR on {request.url}: {error_detail}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    try:
        from app.database import engine, Base
        from app.models.user import User
        from app.models.raw_data import RawData
        from app.models.metrics import CalculatedMetrics
        from app.models.insight import AIInsight
        from app.models.chat import ChatHistory
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
    except Exception as e:
        print(f"⚠️ Database setup: {e}")

# Register routers
try:
    from app.routers import auth, metrics, dashboard, ai, etl
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Metrics"])
    app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
    app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI Insights"])
    app.include_router(etl.router, prefix="/api/v1/etl", tags=["ETL Pipeline"])
    print("✅ All routers registered")
except Exception as e:
    print(f"⚠️ Router error: {e}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "Startup Metrics API", "docs": "/docs"}