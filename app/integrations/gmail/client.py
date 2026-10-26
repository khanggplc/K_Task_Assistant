from googleapiclient.discovery import build
from app.integrations.gmail.oauth import GmailOAuthManager
from app.core.logging import logger


class GmailClient:
    def __init__(self, access_token: str, refresh_token: str | None = None):
        credentials = GmailOAuthManager.get_credentials(access_token, refresh_token)
        self.service = build("gmail", "v1", credentials=credentials, cache_discovery=False)

    def get_profile(self) -> dict:
        try:
            return self.service.users().getProfile(userId="me").execute()
        except Exception as e:
            logger.error("Failed to get Gmail profile: %s", e)
            raise
