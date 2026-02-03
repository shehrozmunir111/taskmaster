from .tasks import router as tasks_router
from .users import router as users_router
from .auth import router as auth_router
from .boards import router as boards_router

__all__ = ["tasks_router", "users_router", "auth_router", "boards_router"]