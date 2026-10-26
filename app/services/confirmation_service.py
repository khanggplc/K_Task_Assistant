from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.repositories.token_repository import TokenRepository
from app.integrations.zalo.client import ZaloClient
from app.integrations.zalo.messages import ZaloMessageService
from app.core.logging import logger


class ConfirmationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.token_repo = TokenRepository(session)

    async def request_confirmation(self, task: Task, external_channel: str = "zalo") -> None:
        """Send interactive confirmation request to user via Zalo or other channels."""
        if external_channel == "zalo":
            token = await self.token_repo.get_token(task.user_id, "zalo")
            if token:
                client = ZaloClient(access_token=token.access_token)
                msg_service = ZaloMessageService(client)
                due_str = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "Chưa xác định"
                await msg_service.send_confirmation_prompt(
                    user_id=task.user_id,
                    task_title=task.title,
                    due_date=due_str
                )
                logger.info("Sent confirmation prompt for task %s via Zalo", task.id)
            else:
                logger.info("No Zalo token found for user %s; skipping external prompt", task.user_id)
