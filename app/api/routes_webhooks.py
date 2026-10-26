import base64
import json
from fastapi import APIRouter, Depends, Header, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.message_service import MessageService
from app.models.message import MessageSource
from app.integrations.zalo.webhook import ZaloWebhookHandler
from app.core.logging import logger

router = APIRouter()


@router.post("/gmail")
async def gmail_push_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Webhook listener for Google Cloud Pub/Sub Gmail inbox notifications."""
    body = await request.json()
    message = body.get("message", {})
    data_b64 = message.get("data")

    if data_b64:
        decoded_data = base64.b64decode(data_b64).decode("utf-8")
        pubsub_payload = json.loads(decoded_data)
        email_address = pubsub_payload.get("emailAddress")
        history_id = pubsub_payload.get("historyId")
        logger.info("Received Gmail notification for %s, historyId: %s", email_address, history_id)

    return {"status": "accepted"}


@router.post("/zalo")
async def zalo_webhook(
    request: Request,
    x_zevent_signature: str = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Webhook listener for Zalo Official Account message events."""
    raw_body = await request.body()
    body_str = raw_body.decode("utf-8")

    if x_zevent_signature:
        if not ZaloWebhookHandler.verify_signature(body_str, x_zevent_signature):
            logger.warning("Invalid Zalo webhook signature!")

    payload = await request.json()
    parsed = ZaloWebhookHandler.parse_event(payload)

    if parsed["text"]:
        service = MessageService(db)
        # Store message to be evaluated by AI background worker
        await service.save_incoming_message(
            user_id=parsed["sender_id"],
            body=parsed["text"],
            source=MessageSource.ZALO,
            sender=parsed["sender_id"],
            external_id=parsed["message_id"],
            raw_payload=body_str,
        )

    return {"error": 0, "message": "Success"}
