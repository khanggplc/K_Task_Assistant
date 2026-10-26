from datetime import datetime, timezone
from app.ai.client import AIClient
from app.ai.prompts import TASK_EXTRACTION_SYSTEM_PROMPT, TASK_EVALUATION_PROMPT
from app.ai.parser import MessageParser
from app.ai.schemas import ActionExtractionResult
from app.core.logging import logger


class TaskEvaluator:
    def __init__(self, ai_client: AIClient | None = None):
        self.client = ai_client or AIClient()
        self.parser = MessageParser()

    async def evaluate_message(
        self,
        content: str,
        sender: str = "",
        subject: str = "",
        reference_time: datetime | None = None
    ) -> ActionExtractionResult:
        now_str = (reference_time or datetime.now(timezone.utc)).isoformat()
        prompt = TASK_EVALUATION_PROMPT.format(
            current_time=now_str,
            sender=sender or "Unknown",
            subject=subject or "No Subject",
            content=content
        )

        logger.info("Evaluating message for actionable tasks: %s", subject or content[:40])
        raw_response = await self.client.generate_completion(
            system_prompt=TASK_EXTRACTION_SYSTEM_PROMPT,
            user_prompt=prompt
        )

        result = self.parser.parse_llm_json(raw_response)
        if not result:
            return ActionExtractionResult(
                is_actionable=False,
                reasoning="Failed to parse actionable content from LLM response.",
                tasks=[]
            )
        return result
