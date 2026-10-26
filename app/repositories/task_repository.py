from typing import Optional, Sequence
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Task:
        task = Task(**kwargs)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalars().first()

    async def get_by_user(self, user_id: str, status: Optional[TaskStatus] = None) -> Sequence[Task]:
        query = select(Task).where(Task.user_id == user_id)
        if status:
            query = query.where(Task.status == status)
        query = query.order_by(Task.due_date.asc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, task_id: str, **kwargs) -> Optional[Task]:
        task = await self.get_by_id(task_id)
        if not task:
            return None
        for key, value in kwargs.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_due_reminders(self, cutoff_time: datetime) -> Sequence[Task]:
        query = (
            select(Task)
            .where(Task.status.in_([TaskStatus.CONFIRMED, TaskStatus.IN_PROGRESS]))
            .where(Task.due_date <= cutoff_time)
            .where(Task.due_date.is_not(None))
        )
        result = await self.session.execute(query)
        return result.scalars().all()
