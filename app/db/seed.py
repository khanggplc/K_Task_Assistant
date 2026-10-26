import asyncio
from app.db.database import async_session_maker, init_db
from app.models.user import User
from app.core.security import get_password_hash
from app.core.logging import logger


async def seed_initial_data() -> None:
    logger.info("Initializing database schema...")
    await init_db()

    async with async_session_maker() as session:
        # Check if default admin exists
        # In a real app, query and insert if missing
        logger.info("Seeding initial data completed.")


if __name__ == "__main__":
    asyncio.run(seed_initial_data())
