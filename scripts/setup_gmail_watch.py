"""Script to initialize or renew Gmail Push Notifications watch via Google Cloud Pub/Sub."""
import asyncio
import sys
from app.db.database import async_session_maker
from app.repositories.token_repository import TokenRepository
from app.integrations.gmail.client import GmailClient
from app.integrations.gmail.watch import GmailWatchManager
from app.core.logging import logger


async def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/setup_gmail_watch.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    async with async_session_maker() as session:
        token_repo = TokenRepository(session)
        token = await token_repo.get_token(user_id=user_id, provider="google")
        if not token:
            logger.error("No Google OAuth token found for user %s", user_id)
            sys.exit(1)

        client = GmailClient(access_token=token.access_token, refresh_token=token.refresh_token)
        watch_mgr = GmailWatchManager(client)
        res = watch_mgr.setup_watch()
        logger.info("Watch setup response: %s", res)


if __name__ == "__main__":
    asyncio.run(main())
