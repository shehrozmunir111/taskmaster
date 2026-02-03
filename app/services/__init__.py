"""
Services Module - Business Logic Layer

This module contains service classes that handle the core business logic
of the application, separating it from the API routes.

Available Services:
    - UserService: Handles user authentication, registration, and management
    - TaskService: Handles task CRUD operations with caching
"""

from app.services.user_service import UserService
from app.services.task_service import TaskService

__all__ = ["UserService", "TaskService"]
