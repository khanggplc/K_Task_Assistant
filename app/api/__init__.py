from fastapi import APIRouter
from app.api.routes_auth import router as auth_router
from app.api.routes_tasks import router as tasks_router
from app.api.routes_messages import router as messages_router
from app.api.routes_webhooks import router as webhooks_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(messages_router, prefix="/messages", tags=["Messages"])
api_router.include_router(webhooks_router, prefix="/webhooks", tags=["Webhooks"])
