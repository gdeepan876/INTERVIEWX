"""
INTERVIEWX – AI Interview Simulator Backend.
Main FastAPI application entry point with CORS, DB initialization, and API routes.
"""

import sys
import os

# Ensure backend directory is in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database.session import Base, engine
from routers.interview_router import router as interview_router

# Ensure tables exist immediately upon import
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that initializes SQLite database tables on startup.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for INTERVIEWX – AI Interview Simulator",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration to allow React frontend (Vite dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(interview_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    """
    Health check endpoint returning system status and evaluation mode.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "database": "SQLite (Connected)",
        "evaluation_mode": "Gemini AI" if (settings.LLM_ENABLED and settings.GEMINI_API_KEY) else "Development Rule-Based Mock",
        "llm_enabled": settings.LLM_ENABLED
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
