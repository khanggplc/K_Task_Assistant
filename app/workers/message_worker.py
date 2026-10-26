import asyncio
from app.db.database import async_session_maker
from app.services.message_service import MessageService
from app.services.task_service import TaskService
from app.services.confirmation_service import ConfirmationService
from app.ai.evaluator import TaskEvaluator
from app.models.message import MessageStatus
from app.core.logging import logger


async def process_pending_messages() -> int:
    """Worker task: picks pending ingested messages, runs AI extraction, and creates tasks."""
    evaluator = TaskEvaluator()
    processed_count = 0

    async with async_session_maker() as session:
        msg_service = MessageService(session)
        task_service = TaskService(session)
        conf_service = ConfirmationService(session)

        messages = await msg_service.get_pending_messages(limit=20)
        for msg in messages:
            try:
                extraction = await evaluator.evaluate_message(
                    content=msg.body,
                    sender=msg.sender or "",
                    subject=msg.subject or ""
                )

                if extraction.is_actionable and extraction.tasks:
                    for item in extraction.tasks:
                        task = await task_service.create_task_from_extraction(
                            user_id=msg.user_id,
                            title=item.title,
                            description=item.description,
                            due_date=item.due_date,
                            priority=item.priority,
                            confidence=item.confidence,
                            message_id=msg.id,
                        )
                        # Optionally notify user via Zalo
                        await conf_service.request_confirmation(task)

                    await msg_service.mark_message_processed(msg.id, MessageStatus.PARSED)
                else:
                    await msg_service.mark_message_processed(msg.id, MessageStatus.IGNORED)

                processed_count += 1
            except Exception as e:
                logger.error("Error processing message %s: %s", msg.id, e)
                await msg_service.mark_message_processed(msg.id, MessageStatus.FAILED)

    return processed_count
