"""
Users API Router - v1

Provides RESTful endpoints for user management operations.
Currently supported: List, Create, Read One, Update, Deactivate, Change Password
"""

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.connection import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate, PasswordChange
from app.services import UserService
from app.core.security import get_current_user, RoleChecker

router = APIRouter()

# Dependency type hints
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
admin_dependency = Annotated[dict, Depends(RoleChecker(["admin"]))]

@router.get("/", response_model=list[UserResponse])
async def read_all_users(db: db_dependency, admin: admin_dependency):
    """
    Retrieve all users. (Admin Only)
    """
    user_service = UserService(db)
    return user_service.get_all_users()


from fastapi import BackgroundTasks
from app.services.notification_service import send_welcome_email

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    db: db_dependency, 
    user_request: UserCreate,
    background_tasks: BackgroundTasks
):
    """
    Register a new user and send a welcome email in the background.
    """
    user_service = UserService(db)
    new_user = user_service.create_user(user_request)
    
    # Add email task to background (Non-blocking)
    background_tasks.add_task(send_welcome_email, new_user.email, new_user.full_name)
    
    return new_user


@router.get("/me", response_model=UserResponse)
async def read_current_user(db: db_dependency, user: user_dependency):
    """
    Get current logged-in user details.
    """
    user_service = UserService(db)
    return user_service.get_user_by_id(user.get('id'))


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    db: db_dependency, 
    user_id: int = Path(gt=0)
):
    """
    Get a specific user by ID.
    """
    from fastapi import HTTPException
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    db: db_dependency,
    user: user_dependency,  # Require auth
    user_update: UserUpdate,
    user_id: int = Path(gt=0)
):
    """
    Update user profile.
    
    Only allows updating: full_name, email
    """
    from fastapi import HTTPException
    
    # Optional: Check if user is updating themselves or is admin
    if user.get('id') != user_id:
         raise HTTPException(status_code=403, detail="Not authorized to update this user")

    user_service = UserService(db)
    # Convert Pydantic model to dict, removing None values
    update_data = user_update.model_dump(exclude_unset=True)
    return user_service.update_user(user_id, **update_data)


@router.delete("/{user_id}", response_model=UserResponse)
async def deactivate_user(
    db: db_dependency,
    user: user_dependency, # Require auth
    user_id: int = Path(gt=0)
):
    """
    Deactivate a user account (Soft delete).
    """
    from fastapi import HTTPException

    if user.get('id') != user_id:
         raise HTTPException(status_code=403, detail="Not authorized to deactivate this user")
         
    user_service = UserService(db)
    return user_service.deactivate_user(user_id)


@router.post("/change-password")
async def change_password(
    db: db_dependency,
    user: user_dependency,
    password_data: PasswordChange
):
    """
    Change user password.
    """
    user_service = UserService(db)
    user_service.change_password(
        user_id=user.get('id'),
        old_password=password_data.old_password,
        new_password=password_data.new_password
    )
    return {"message": "Password updated successfully"}
