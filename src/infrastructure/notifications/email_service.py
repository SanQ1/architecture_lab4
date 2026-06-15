from src.application.notifications.abstract_notification import AbstractNotificationService
import time

class EmailNotificationService(AbstractNotificationService):
    def send(self, user_email: str, message: str) -> None:
        time.sleep(3)
        print(f"{user_email}: {message}")
