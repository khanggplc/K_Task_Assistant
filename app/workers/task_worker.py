from app.db.database import async_session_maker
from app.services.reminder_service import ReminderService
from app.core.logging import logger


async def process_reminders() -> int:
    """Worker job: Checks upcoming deadlines and triggers notification reminders."""
    async with async_session_maker() as session:
        service = ReminderService(session)
        reminders_sent = await service.check_and_send_due_reminders(window_minutes=60)
        if reminders_sent > 0:
            logger.info("Sent %d due task reminders.", reminders_sent)
        return reminders_sent
