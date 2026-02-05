"""
Boards API Router - v1
"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.db.connection import get_db
from app.core.security import get_current_user
from app.schemas.board import BoardResponse, BoardCreate, LaneCreate, LaneResponse, LaneUpdate
from app.services.board_service import BoardService

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# --- BOARDS ---

@router.post("/", response_model=BoardResponse)
async def create_board(board: BoardCreate, db: db_dependency, user: user_dependency):
    service = BoardService(db, user.get('id'))
    return service.create_board(board)

@router.get("/", response_model=List[BoardResponse])
async def get_boards(db: db_dependency, user: user_dependency):
    service = BoardService(db, user.get('id'))
    return service.get_my_boards()

@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(db: db_dependency, user: user_dependency, board_id: int):
    service = BoardService(db, user.get('id'))
    return service.get_board(board_id)

@router.delete("/{board_id}")
async def delete_board(db: db_dependency, user: user_dependency, board_id: int):
    service = BoardService(db, user.get('id'))
    return service.delete_board(board_id)

# --- LANES (Nested under Boards) ---

@router.post("/{board_id}/lanes", response_model=LaneResponse)
async def create_lane(
    board_id: int, 
    lane: LaneCreate, 
    db: db_dependency, 
    user: user_dependency
):
    service = BoardService(db, user.get('id'))
    return service.create_lane(board_id, lane)

@router.put("/lanes/{lane_id}", response_model=LaneResponse)
async def update_lane(
    lane_id: int,
    lane: LaneUpdate,
    db: db_dependency,
    user: user_dependency
):
    service = BoardService(db, user.get('id'))
    return service.update_lane(lane_id, lane)

@router.delete("/lanes/{lane_id}")
async def delete_lane(
    lane_id: int,
    db: db_dependency,
    user: user_dependency
):
    service = BoardService(db, user.get('id'))
    return service.delete_lane(lane_id)
