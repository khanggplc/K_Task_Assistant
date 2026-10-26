from typing import Dict, Any, Optional
from app.integrations.gmail.client import GmailClient
from app.core.config import settings
from app.core.logging import logger


class GmailWatchManager:
    def __init__(self, client: GmailClient):
        self.service = client.service

    def setup_watch(self, topic_name: Optional[str] = None) -> Dict[str, Any]:
        """Register Gmail push notifications to Google Cloud Pub/Sub topic."""
        target_topic = topic_name or settings.GOOGLE_PUBSUB_TOPIC
        if not target_topic:
            raise ValueError("Google Cloud Pub/Sub topic name is required to setup watch.")

        request_body = {
            "labelIds": ["INBOX"],
            "topicName": target_topic
        }
        try:
            response = self.service.users().watch(userId="me", body=request_body).execute()
            logger.info("Successfully set up Gmail watch: %s", response)
            return response
        except Exception as e:
            logger.error("Failed to setup Gmail watch: %s", e)
            raise

    def stop_watch(self) -> None:
        try:
            self.service.users().stop(userId="me").execute()
            logger.info("Gmail watch stopped successfully.")
        except Exception as e:
            logger.error("Failed to stop Gmail watch: %s", e)
            raise
