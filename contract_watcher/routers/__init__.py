from .auth import router as auth_router
from .history import router as history_router
from .webhooks import router as webhooks_router

members = (
    auth_router,
    history_router,
    webhooks_router
)
