"""
Tasks (Cards) API Router - v1

Provides RESTful endpoints for task (card) management operations.
"""

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from typing import Annotated

from app.core.security import get_current_user
from app.db.connection import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import TaskService

router = APIRouter()

# Dependency type hints
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task: TaskCreate,
    db: db_dependency,
    user: user_dependency
) -> TaskResponse:
    """Create a new task (card) in a specific lane."""
    service = TaskService(db, user.get('id'))
    return service.create_task(task)

@router.delete("/{task_id}")
async def delete_task(
    db: db_dependency,
    user: user_dependency,
    task_id: int = Path(gt=0)
) -> dict:
    """Delete a task."""
    service = TaskService(db, user.get('id'))
    return service.delete_task(task_id)

@router.put("/{task_id}/move", response_model=TaskResponse)
async def move_task_card(
    db: db_dependency,
    user: user_dependency,
    task_id: int = Path(gt=0),
    new_lane_id: int = Body(..., embed=True),
    new_position: int = Body(..., embed=True)
) -> TaskResponse:
    """
    Move a task to a different lane or reorder it.
    
    This is the primary endpoint for drag-and-drop actions.
    """
    service = TaskService(db, user.get('id'))
    return service.move_task(task_id, new_lane_id, new_position) # Corrected wrapper usage

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_details(
    db: db_dependency,
    user: user_dependency,
    task: TaskUpdate,
    task_id: int = Path(gt=0)
) -> TaskResponse:
    """
    Update task details (title, description, priority).
    """
    service = TaskService(db, user.get('id'))
    return service.update_task(task_id, task)