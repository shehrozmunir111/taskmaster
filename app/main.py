"""
TaskMaster API - Main Application Entry Point

A professional task management REST API built with FastAPI.
Features:
- JWT Authentication
- PostgreSQL database with SQLAlchemy ORM
- Redis caching for optimized performance
- RESTful API design with versioning
"""

from fastapi import FastAPI
from app.core.config import settings
from app.db.connection import Base, engine
from app.api.v1 import tasks_router, users_router, auth_router, boards_router

# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A professional task management API",
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers with API versioning
app.include_router(auth_router, tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(boards_router, prefix="/boards", tags=["Boards"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])

# Create database tables
Base.metadata.create_all(bind=engine)


# ========================
# Health Check Endpoints
# ========================

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        Health status message
    """
    return {"status": "healthy", "app_name": settings.app_name}


# ========================
# Startup Events
# ========================

@app.on_event("startup")
async def startup_event():
    """Initialize resources on application startup."""
    # You can add database connection checks, cache warming, etc.
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on application shutdown."""
    from app.core.cache import CacheClient
    CacheClient.close()
