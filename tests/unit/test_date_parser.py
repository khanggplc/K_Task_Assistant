from datetime import datetime
from app.ai.schemas import ExtractedTask


def test_extracted_task_date_parsing():
    task = ExtractedTask(
        title="Deploy release",
        due_date="2026-10-30T10:00:00Z"
    )
    assert isinstance(task.due_date, datetime)
    assert task.due_date.year == 2026
    assert task.due_date.month == 10
    assert task.due_date.day == 30
