"""
Board Service - Business logic for Boards and Lanes.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.board import Board, Lane
from app.schemas.board import BoardCreate, LaneCreate, LaneUpdate

class BoardService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    # --- BOARD OPERATIONS ---
    def create_board(self, board_data: BoardCreate) -> Board:
        new_board = Board(
            **board_data.model_dump(),
            owner_id=self.user_id
        )
        self.db.add(new_board)
        self.db.commit()
        self.db.refresh(new_board)
        
        # Create default lanes for a new board
        default_lanes = ["Todo", "In Progress", "Done"]
        for i, title in enumerate(default_lanes):
            lane = Lane(title=title, board_id=new_board.id, position=i)
            self.db.add(lane)
        
        self.db.commit()
        self.db.refresh(new_board)
        return new_board

    def get_my_boards(self) -> List[Board]:
        return self.db.query(Board).filter(Board.owner_id == self.user_id).all()

    def get_board(self, board_id: int) -> Board:
        board = self.db.query(Board).filter(
            Board.id == board_id,
            Board.owner_id == self.user_id
        ).first()
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        return board
    
    def delete_board(self, board_id: int):
        board = self.get_board(board_id)
        self.db.delete(board)
        self.db.commit()
        return {"message": "Board deleted"}

    # --- LANE OPERATIONS ---
    def create_lane(self, board_id: int, lane_data: LaneCreate) -> Lane:
        # Verify board ownership
        self.get_board(board_id) 
        
        new_lane = Lane(
            **lane_data.model_dump(),
            board_id=board_id
        )
        self.db.add(new_lane)
        self.db.commit()
        self.db.refresh(new_lane)
        return new_lane

    def update_lane(self, lane_id: int, lane_data: LaneUpdate) -> Lane:
        lane = self.db.query(Lane).filter(Lane.id == lane_id).first()
        if not lane:
            raise HTTPException(status_code=404, detail="Lane not found")
        
        # Verify board ownership (via lane -> board)
        if lane.board.owner_id != self.user_id:
            raise HTTPException(status_code=403, detail="Not authorized")

        update_data = lane_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(lane, key, value)
            
        self.db.commit()
        self.db.refresh(lane)
        return lane
        
    def delete_lane(self, lane_id: int):
        lane = self.db.query(Lane).filter(Lane.id == lane_id).first()
        if not lane:
            raise HTTPException(status_code=404, detail="Lane not found")
        
        if lane.board.owner_id != self.user_id:
             raise HTTPException(status_code=403, detail="Not authorized")
             
        self.db.delete(lane)
        self.db.commit()
        return {"message": "Lane deleted"}
