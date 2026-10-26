from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.task_service import TaskService
from app.models.task import TaskPriority, TaskStatus

router = APIRouter()


class TaskCreateRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"
    confidence: int = 100


class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    priority: TaskPriority
    status: TaskStatus
    google_event_id: Optional[str]

    model_config = ConfigDict(from_attributes=True)



@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str,
    status: Optional[TaskStatus] = None,
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    tasks = await service.list_tasks(user_id=user_id, status=status)
    return tasks


@router.post("/", response_model=TaskResponse)
async def create_task(
    payload: TaskCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    task = await service.create_task_from_extraction(
        user_id=payload.user_id,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        priority=payload.priority,
        confidence=payload.confidence,
    )
    return task


@router.post("/{task_id}/confirm", response_model=TaskResponse)
async def confirm_task(
    task_id: str,
    sync_calendar: bool = True,
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    task = await service.confirm_task(task_id=task_id, sync_calendar=sync_calendar)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
