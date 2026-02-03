from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.connection import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user") # 'admin', 'user', 'manager'

    created_at = Column(DateTime, server_default=func.now())
    tasks = relationship("Task", back_populates="owner")
    boards = relationship("Board", back_populates="owner")
