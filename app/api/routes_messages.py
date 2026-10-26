from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.message_service import MessageService
from app.models.message import MessageSource, MessageStatus

router = APIRouter()


class IngestMessageRequest(BaseModel):
    user_id: str
    body: str
    source: MessageSource = MessageSource.MANUAL
    sender: Optional[str] = None
    recipient: Optional[str] = None
    subject: Optional[str] = None
    external_id: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    user_id: str
    source: MessageSource
    subject: Optional[str]
    sender: Optional[str]
    status: MessageStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



@router.post("/ingest", response_model=MessageResponse)
async def ingest_message(
    payload: IngestMessageRequest,
    db: AsyncSession = Depends(get_db),
):
    service = MessageService(db)
    message = await service.save_incoming_message(
        user_id=payload.user_id,
        body=payload.body,
        source=payload.source,
        sender=payload.sender,
        recipient=payload.recipient,
        subject=payload.subject,
        external_id=payload.external_id,
    )
    return message
