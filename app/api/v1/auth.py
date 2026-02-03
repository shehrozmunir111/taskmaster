"""
Authentication API Router - v1

Provides endpoints for user authentication.
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.connection import get_db
from app.services import UserService

router = APIRouter()

# Dependency type hints
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/login")
async def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and obtain JWT token.
    
    Uses OAuth2 password flow. Username field expects the user's email.
    
    Args:
        form_data: OAuth2 password request form (username=email, password)
        
    Returns:
        Access token and token type
        
    Raises:
        HTTPException 401: If credentials are invalid
    """
    user_service = UserService(db)
    return user_service.login(
        email=form_data.username,
        password=form_data.password
    )
