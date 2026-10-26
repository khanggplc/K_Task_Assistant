import hashlib
import hmac
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger


class ZaloWebhookHandler:
    @staticmethod
    def verify_signature(data: str, signature: str, secret_key: Optional[str] = None) -> bool:
        secret = secret_key or settings.ZALO_WEBHOOK_SECRET or settings.ZALO_OA_SECRET_KEY
        if not secret:
            logger.warning("No Zalo secret configured to verify signature.")
            return True

        expected_sig = "mac=" + hmac.new(
            secret.encode("utf-8"), data.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_sig, signature)

    @staticmethod
    def parse_event(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Zalo OA webhook payload into standard message format."""
        event_name = payload.get("event_name", "")
        sender_id = payload.get("sender", {}).get("id", "")
        recipient_id = payload.get("recipient", {}).get("id", "")
        message_data = payload.get("message", {})

        text = message_data.get("text", "")
        msg_id = message_data.get("msg_id", "")

        return {
            "event_name": event_name,
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "message_id": msg_id,
            "text": text,
            "timestamp": payload.get("timestamp"),
            "raw": payload
        }
