from unittest.mock import MagicMock, patch
from app.integrations.gmail.messages import GmailMessageService


def test_gmail_message_listing_mock():
    mock_client = MagicMock()
    mock_messages_resource = MagicMock()
    mock_client.service.users().messages.return_value = mock_messages_resource

    mock_messages_resource.list.return_value.execute.return_value = {
        "messages": [{"id": "123", "threadId": "456"}]
    }

    service = GmailMessageService(mock_client)
    msgs = service.list_unread_messages()

    assert len(msgs) == 1
    assert msgs[0]["id"] == "123"
