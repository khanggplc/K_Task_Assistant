from typing import Dict, Any, Optional
import httpx
from app.core.config import settings
from app.core.logging import logger

ZALO_OA_API_BASE = "https://openapi.zalo.me/v3.0/oa"


class ZaloClient:
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self.app_id = settings.ZALO_APP_ID
        self.app_secret = settings.ZALO_APP_SECRET

    async def get_access_token_from_code(self, oauth_code: str, code_verifier: str) -> Dict[str, Any]:
        url = "https://oauth.zaloapp.com/v4/oa/access_token"
        headers = {
            "secret_key": self.app_secret,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "code": oauth_code,
            "app_id": self.app_id,
            "grant_type": "authorization_code",
            "code_verifier": code_verifier
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(url, headers=headers, data=data)
            res.raise_for_status()
            return res.json()

    async def send_text_message(self, user_id: str, text: str) -> Dict[str, Any]:
        """Send message to a Zalo OA follower."""
        url = f"{ZALO_OA_API_BASE}/message/cs"
        headers = {
            "access_token": self.access_token or "",
            "Content-Type": "application/json"
        }
        payload = {
            "recipient": {"user_id": user_id},
            "message": {"text": text}
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(url, headers=headers, json=payload)
            res.raise_for_status()
            logger.info("Sent Zalo message to user %s", user_id)
            return res.json()
