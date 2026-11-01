from app.routers.health import router as health_router
from app.routers.applications import router as applications_router
from app.routers.contacts import router as contacts_router
from app.routers.auth import router as auth_router

__all__ = [
    "health_router",
    "applications_router",
    "contacts_router",
    "auth_router",
]
