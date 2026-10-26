from app.integrations.zalo.client import ZaloClient
from app.core.logging import logger


class ZaloMessageService:
    def __init__(self, client: ZaloClient):
        self.client = client

    async def send_confirmation_prompt(self, user_id: str, task_title: str, due_date: str) -> None:
        message_text = (
            f"🔔 [Task Assistant] Có một công việc mới được phát hiện:\n"
            f"📌 Tiêu đề: {task_title}\n"
            f"⏰ Thời hạn: {due_date}\n\n"
            f"Vui lòng phản hồi 'Xác nhận' để đưa vào lịch hoặc 'Hủy' để bỏ qua."
        )
        await self.client.send_text_message(user_id=user_id, text=message_text)

    async def send_reminder(self, user_id: str, task_title: str, due_date: str) -> None:
        message_text = f"⏰ [Nhắc nhở] Công việc '{task_title}' sắp đến hạn vào {due_date}!"
        await self.client.send_text_message(user_id=user_id, text=message_text)
