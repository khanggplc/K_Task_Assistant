import json
from typing import Optional
from app.ai.schemas import ActionExtractionResult
from app.core.logging import logger


class MessageParser:
    @staticmethod
    def parse_llm_json(raw_text: str) -> Optional[ActionExtractionResult]:
        """Parses LLM JSON response string into validated ActionExtractionResult."""
        try:
            # Strip markdown code blocks if returned
            cleaned = raw_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            parsed_data = json.loads(cleaned)
            return ActionExtractionResult(**parsed_data)
        except Exception as e:
            logger.error("Failed to parse AI output into schema: %s. Raw: %s", e, raw_text)
            return None
