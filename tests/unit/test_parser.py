import pytest
from app.ai.parser import MessageParser


def test_parse_valid_llm_json():
    raw_json = """
    ```json
    {
        "is_actionable": true,
        "reasoning": "Explicit deadline mentioned",
        "tasks": [
            {
                "title": "Submit Q3 Report",
                "description": "Financial summaries needed",
                "due_date": "2026-10-25T17:00:00Z",
                "priority": "high",
                "confidence": 95,
                "assignee": "Alex"
            }
        ]
    }
    ```
    """
    res = MessageParser.parse_llm_json(raw_json)
    assert res is not None
    assert res.is_actionable is True
    assert len(res.tasks) == 1
    assert res.tasks[0].title == "Submit Q3 Report"
    assert res.tasks[0].priority == "high"


def test_parse_invalid_json():
    raw_invalid = "Sorry, I am an AI language model and cannot output JSON."
    res = MessageParser.parse_llm_json(raw_invalid)
    assert res is None
