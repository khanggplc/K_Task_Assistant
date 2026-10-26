import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from app.services.task_service import TaskService
from app.models.task import Task, TaskStatus, TaskPriority


@pytest.mark.asyncio
async def test_create_task_from_extraction():
    mock_session = AsyncMock()
    service = TaskService(mock_session)

    dummy_task = Task(
        id="task_123",
        user_id="user_1",
        title="Test Task",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PENDING_CONFIRMATION,
    )
    service.repo.create = AsyncMock(return_value=dummy_task)

    task = await service.create_task_from_extraction(
        user_id="user_1",
        title="Test Task",
        priority="high",
        confidence=90,
    )

    assert task.id == "task_123"
    assert task.title == "Test Task"
    service.repo.create.assert_awaited_once()
