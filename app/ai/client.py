from typing import Optional, Any
import json
import httpx
from app.core.config import settings
from app.core.logging import logger


class AIClient:
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL_NAME

    async def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Optional[dict[str, Any]] = None
    ) -> str:
        """Call AI provider. If no API key is provided, returns mock demonstration JSON."""
        if not self.api_key:
            logger.warning("AI_API_KEY is not set. Generating mock response for development.")
            return json.dumps({
                "is_actionable": True,
                "reasoning": "Mock evaluation: message detected actionable request.",
                "tasks": [
                    {
                        "title": "Review project deliverables",
                        "description": "Auto-extracted task from message context",
                        "due_date": "2026-10-20T17:00:00Z",
                        "priority": "high",
                        "confidence": 95,
                        "assignee": "team"
                    }
                ]
            })

        # OpenAI compatible endpoint
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
