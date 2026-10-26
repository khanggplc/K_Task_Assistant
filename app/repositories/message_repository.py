from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message, MessageStatus


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Message:
        message = Message(**kwargs)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_by_id(self, message_id: str) -> Optional[Message]:
        result = await self.session.execute(select(Message).where(Message.id == message_id))
        return result.scalars().first()

    async def get_by_external_id(self, external_id: str) -> Optional[Message]:
        result = await self.session.execute(select(Message).where(Message.external_id == external_id))
        return result.scalars().first()

    async def get_pending_messages(self, limit: int = 50) -> Sequence[Message]:
        result = await self.session.execute(
            select(Message).where(Message.status == MessageStatus.PENDING).limit(limit)
        )
        return result.scalars().all()

    async def update_status(self, message_id: str, status: MessageStatus) -> Optional[Message]:
        message = await self.get_by_id(message_id)
        if message:
            message.status = status
            await self.session.commit()
            await self.session.refresh(message)
        return message
