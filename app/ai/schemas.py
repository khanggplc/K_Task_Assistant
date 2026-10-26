from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ExtractedTask(BaseModel):
    title: str = Field(description="Brief title/action for the task")
    description: Optional[str] = Field(default=None, description="Detailed context or notes")
    due_date: Optional[datetime] = Field(default=None, description="ISO format datetime if identified")
    priority: str = Field(default="medium", description="Priority: low, medium, high, urgent")
    confidence: int = Field(default=80, description="Confidence score from 0 to 100")
    assignee: Optional[str] = Field(default=None, description="Person assigned or requested")


class ActionExtractionResult(BaseModel):
    is_actionable: bool = Field(description="Whether the message contains an actionable task or calendar event")
    reasoning: str = Field(description="Explanation of why this is or isn't actionable")
    tasks: List[ExtractedTask] = Field(default_factory=list, description="List of tasks identified in the message")
