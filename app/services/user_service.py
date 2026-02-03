"""
User Service - Business logic for user operations.

This service layer handles all user-related business logic,
separating it from the API routes for better maintainability and testability.
"""

from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


class UserService:
    """Service class for user-related operations."""
    
    def __init__(self, db: Session):
        """
        Initialize the UserService with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        
        Args:
            email: User's email address
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: User's database ID
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_all_users(self) -> list[User]:
        """
        Retrieve all users from the database.
        
        Returns:
            List of all User objects
        """
        return self.db.query(User).all()
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user account.
        
        Args:
            user_data: Pydantic schema containing user registration data
            
        Returns:
            Newly created User object
            
        Raises:
            HTTPException: If email is already registered
        """
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )
        
        # Hash the password
        hashed_password = hash_password(user_data.password)
        
        # Create new user instance
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        
        # Save to database
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return new_user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            User object if authentication succeeds, None otherwise
        """
        user = self.get_user_by_email(email)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def login(self, email: str, password: str) -> dict:
        """
        Authenticate user and generate JWT token.
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            Dictionary containing access_token and token_type
            
        Raises:
            HTTPException: If credentials are invalid
        """
        user = self.authenticate_user(email, password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Create access token
        token_expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            email=user.email,
            user_id=user.id,
            role=user.role,
            expires_delta=token_expiry
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    def update_user(self, user_id: int, **kwargs) -> User:
        """
        Update user information.
        
        Args:
            user_id: User's database ID
            **kwargs: Fields to update (full_name, email, etc.)
            
        Returns:
            Updated User object
            
        Raises:
            HTTPException: If user not found
        """
        user = self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found."
            )
        
        # Update allowed fields
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def deactivate_user(self, user_id: int) -> User:
        """
        Deactivate a user account.
        
        Args:
            user_id: User's database ID
            
        Returns:
            Updated User object
            
        Raises:
            HTTPException: If user not found
        """
        user = self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found."
            )
        
        user.is_active = False
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change user's password.
        
        Args:
            user_id: User's database ID
            old_password: Current password
            new_password: New password
            
        Returns:
            True if password changed successfully
            
        Raises:
            HTTPException: If user not found or old password is incorrect
        """
        user = self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found."
            )
        
        # Verify old password
        if not verify_password(old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect."
            )
        
        # Hash and save new password
        user.hashed_password = hash_password(new_password)
        self.db.commit()
        
        return True
