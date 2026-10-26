import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.workers.message_worker import process_pending_messages
from app.workers.task_worker import process_reminders
from app.core.config import settings
from app.core.logging import logger

scheduler = AsyncIOScheduler()


def start_scheduler() -> AsyncIOScheduler:
    """Schedule background worker tasks."""
    scheduler.add_job(
        process_pending_messages,
        "interval",
        seconds=settings.POLL_INTERVAL_SECONDS,
        id="process_messages_job",
        replace_existing=True,
    )
    scheduler.add_job(
        process_reminders,
        "interval",
        minutes=5,
        id="process_reminders_job",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Background APScheduler started.")
    return scheduler


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Background APScheduler stopped.")
