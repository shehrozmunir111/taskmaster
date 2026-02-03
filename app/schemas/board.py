from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.task import TaskResponse

# --- Lane Schemas ---
class LaneBase(BaseModel):
    title: str
    position: int = 0

class LaneCreate(LaneBase):
    pass

class LaneUpdate(BaseModel):
    title: Optional[str] = None
    position: Optional[int] = None

class LaneResponse(LaneBase):
    id: int
    board_id: int
    tasks: List[TaskResponse] = [] # Nested tasks

    class Config:
        from_attributes = True

# --- Board Schemas ---
class BoardBase(BaseModel):
    title: str
    description: Optional[str] = None

class BoardCreate(BoardBase):
    pass

class BoardResponse(BoardBase):
    id: int
    owner_id: int
    created_at: datetime
    lanes: List[LaneResponse] = [] # Nested lanes with tasks

    class Config:
        from_attributes = True
