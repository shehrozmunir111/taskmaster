from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.connection import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    
    # Trello-specific fields
    position = Column(Integer, default=0)  # Order of card in the list
    priority = Column(Integer, default=1)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Task belongs to a specific Lane (List)
    lane_id = Column(Integer, ForeignKey("lanes.id"), nullable=True)
    lane = relationship("Lane", back_populates="tasks")

    # Access to Board directly (optional but useful)
    # owner_id is kept for tracking who created it, or who is assigned
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")