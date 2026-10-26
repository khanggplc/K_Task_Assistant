from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.token_repository import TokenRepository
from app.integrations.zalo.client import ZaloClient
from app.integrations.zalo.messages import ZaloMessageService
from app.core.logging import logger


class ReminderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.task_repo = TaskRepository(session)
        self.token_repo = TokenRepository(session)

    async def check_and_send_due_reminders(self, window_minutes: int = 60) -> int:
        """Finds upcoming tasks within the window and sends notifications."""
        cutoff_time = datetime.now(timezone.utc) + timedelta(minutes=window_minutes)
        tasks = await self.task_repo.get_due_reminders(cutoff_time=cutoff_time)

        count = 0
        for task in tasks:
            token = await self.token_repo.get_token(task.user_id, "zalo")
            if token:
                client = ZaloClient(access_token=token.access_token)
                msg_service = ZaloMessageService(client)
                due_str = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "Sớm"
                try:
                    await msg_service.send_reminder(
                        user_id=task.user_id,
                        task_title=task.title,
                        due_date=due_str
                    )
                    count += 1
                except Exception as e:
                    logger.error("Failed to send reminder for task %s: %s", task.id, e)

        return count
