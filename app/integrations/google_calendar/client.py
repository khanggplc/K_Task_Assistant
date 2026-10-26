from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from app.integrations.gmail.oauth import GmailOAuthManager
from app.core.logging import logger


class GoogleCalendarClient:
    def __init__(self, access_token: str, refresh_token: Optional[str] = None):
        credentials = GmailOAuthManager.get_credentials(access_token, refresh_token)
        self.service = build("calendar", "v3", credentials=credentials, cache_discovery=False)

    def create_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a scheduled event in user's primary Google Calendar."""
        if not end_time:
            end_time = start_time + timedelta(hours=1)

        event_body = {
            "summary": summary,
            "description": description or "",
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "UTC",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 30},
                    {"method": "email", "minutes": 60},
                ],
            },
        }

        try:
            event = self.service.events().insert(calendarId="primary", body=event_body).execute()
            logger.info("Created Google Calendar event: %s (%s)", summary, event.get("id"))
            return event
        except Exception as e:
            logger.error("Failed to create Google Calendar event: %s", e)
            raise
