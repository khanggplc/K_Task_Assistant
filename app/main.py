import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Đảm bảo thư mục gốc dự án luôn có trong sys.path để có thể chạy trực tiếp bằng nút Run (Play) trên IDE
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.db.database import init_db
from app.api import api_router
from app.workers.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up %s...", settings.APP_NAME)
    # Khởi tạo bảng cơ sở dữ liệu
    await init_db()
    # Khởi động bộ lập lịch tác vụ nền
    start_scheduler()
    yield
    # Dừng an toàn khi tắt app
    logger.info("Shutting down %s...", settings.APP_NAME)
    stop_scheduler()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Intelligent AI Task Assistant with Gmail, Zalo, and Google Calendar integrations",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn các router API
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
