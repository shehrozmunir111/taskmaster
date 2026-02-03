from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 1
    lane_id: int  # Task must belong to a lane
    position: int = 0  # Default to top/bottom

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    created_at: datetime
    owner_id: int
    
    lane_id: Optional[int] = None
    position: int

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    lane_id: Optional[int] = None  # For moving to another column
    position: Optional[int] = None  # For reordering