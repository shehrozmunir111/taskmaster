"""
Task Service - Business logic for task (Card) operations.
"""

from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.board import Lane, Board
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
    
    def _verify_lane_access(self, lane_id: int):
        """Ensure the user owns the board that contains this lane."""
        lane = self.db.query(Lane).join(Board).filter(
            Lane.id == lane_id,
            Board.owner_id == self.user_id
        ).first()
        
        if not lane:
            raise HTTPException(
                status_code=400,
                detail="Invalid Lane ID or you don't have access to this board."
            )
        return lane

    def create_task(self, task_data: TaskCreate) -> Task:
        # Verify lane access
        self._verify_lane_access(task_data.lane_id)
        
        new_task = Task(
            **task_data.model_dump(),
            owner_id=self.user_id
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.owner_id == self.user_id
        ).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # If moving to a new lane, verify access
        if task_data.lane_id:
            self._verify_lane_access(task_data.lane_id)

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.owner_id == self.user_id
        ).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
            
        self.db.delete(task)
        self.db.commit()
        return {"message": "Task deleted"}
    
    def move_task(self, task_id: int, new_lane_id: int, new_position: int) -> Task:
        """ Specialized method for drag-and-drop updates """
        return self.update_task(task_id, TaskUpdate(lane_id=new_lane_id, position=new_position))
