from typing import Optional, Sequence
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.token_repository import TokenRepository
from app.models.task import Task, TaskStatus, TaskPriority
from app.integrations.google_calendar.client import GoogleCalendarClient
from app.core.logging import logger


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)
        self.token_repo = TokenRepository(session)

    async def create_task_from_extraction(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: str = "medium",
        confidence: int = 100,
        message_id: Optional[str] = None,
    ) -> Task:
        p_enum = getattr(TaskPriority, priority.upper(), TaskPriority.MEDIUM)
        task = await self.repo.create(
            user_id=user_id,
            message_id=message_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=p_enum,
            confidence_score=confidence,
            status=TaskStatus.PENDING_CONFIRMATION,
        )
        return task

    async def confirm_task(self, task_id: str, sync_calendar: bool = True) -> Optional[Task]:
        task = await self.repo.get_by_id(task_id)
        if not task:
            return None

        event_id = None
        if sync_calendar and task.due_date:
            token = await self.token_repo.get_token(task.user_id, "google")
            if token:
                try:
                    cal_client = GoogleCalendarClient(token.access_token, token.refresh_token)
                    event = cal_client.create_event(
                        summary=task.title,
                        start_time=task.due_date,
                        description=task.description,
                    )
                    event_id = event.get("id")
                except Exception as e:
                    logger.error("Failed to sync task %s with Google Calendar: %s", task_id, e)

        return await self.repo.update(
            task_id=task_id,
            status=TaskStatus.CONFIRMED,
            google_event_id=event_id,
        )

    async def list_tasks(self, user_id: str, status: Optional[TaskStatus] = None) -> Sequence[Task]:
        return await self.repo.get_by_user(user_id=user_id, status=status)
