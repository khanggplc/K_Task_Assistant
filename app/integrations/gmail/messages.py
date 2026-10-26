import base64
from typing import List, Dict, Any, Optional
from app.integrations.gmail.client import GmailClient
from app.core.logging import logger


class GmailMessageService:
    def __init__(self, client: GmailClient):
        self.client = client
        self.service = client.service

    def list_unread_messages(self, max_results: int = 10) -> List[Dict[str, Any]]:
        try:
            results = self.service.users().messages().list(
                userId="me", q="is:unread", maxResults=max_results
            ).execute()
            return results.get("messages", [])
        except Exception as e:
            logger.error("Error listing unread Gmail messages: %s", e)
            return []

    def get_message_detail(self, message_id: str) -> Optional[Dict[str, Any]]:
        try:
            message = self.service.users().messages().get(
                userId="me", id=message_id, format="full"
            ).execute()

            headers = {
                h["name"].lower(): h["value"]
                for h in message.get("payload", {}).get("headers", [])
            }

            body = ""
            payload = message.get("payload", {})
            if "parts" in payload:
                for part in payload["parts"]:
                    if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break
            elif "body" in payload and "data" in payload["body"]:
                body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

            return {
                "id": message["id"],
                "thread_id": message.get("threadId"),
                "subject": headers.get("subject", "No Subject"),
                "sender": headers.get("from", "Unknown"),
                "recipient": headers.get("to", ""),
                "date": headers.get("date"),
                "snippet": message.get("snippet", ""),
                "body": body or message.get("snippet", ""),
            }
        except Exception as e:
            logger.error("Error fetching message detail for %s: %s", message_id, e)
            return None

    def mark_as_read(self, message_id: str) -> None:
        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()
        except Exception as e:
            logger.error("Error marking message %s as read: %s", message_id, e)
