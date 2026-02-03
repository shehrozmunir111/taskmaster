from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.connection import Base

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="boards")
    
    # Relationships
    lanes = relationship("Lane", back_populates="board", cascade="all, delete-orphan")


class Lane(Base):
    """Represents a column/list in Trello (e.g. Todo, Done)"""
    __tablename__ = "lanes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    position = Column(Integer, default=0) # To order columns (0, 1, 2...)
    
    board_id = Column(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="lanes")
    
    # Relationships
    tasks = relationship("Task", back_populates="lane", cascade="all, delete-orphan")
