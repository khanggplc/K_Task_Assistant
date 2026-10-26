from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.message_repository import MessageRepository
from app.models.message import Message, MessageSource, MessageStatus
from app.ai.evaluator import TaskEvaluator
from app.core.logging import logger


class MessageService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = MessageRepository(session)
        self.evaluator = TaskEvaluator()

    async def save_incoming_message(
        self,
        user_id: str,
        body: str,
        source: MessageSource,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        subject: Optional[str] = None,
        external_id: Optional[str] = None,
        raw_payload: Optional[str] = None,
    ) -> Message:
        # Check deduplication
        if external_id:
            existing = await self.repo.get_by_external_id(external_id)
            if existing:
                logger.info("Message %s already ingested. Skipping duplicate.", external_id)
                return existing

        message = await self.repo.create(
            user_id=user_id,
            body=body,
            source=source,
            sender=sender,
            recipient=recipient,
            subject=subject,
            external_id=external_id,
            raw_payload=raw_payload,
            status=MessageStatus.PENDING,
        )
        return message

    async def get_pending_messages(self, limit: int = 50) -> Sequence[Message]:
        return await self.repo.get_pending_messages(limit=limit)

    async def mark_message_processed(self, message_id: str, status: MessageStatus) -> None:
        await self.repo.update_status(message_id, status)
