"""Script to run database schema migrations or initialization."""
import asyncio
from app.db.database import init_db
from app.core.logging import logger


async def main():
    logger.info("Running database migration...")
    await init_db()
    logger.info("Database migration completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
