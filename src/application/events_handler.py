from src.application.notifications.abstract_notification import AbstractNotificationService
from src.application.events import OrderCreated

class NotificationEventHandler:
    def __init__(self, notification_service):
        self.notification_service = notification_service

    def on_order_created(self, event: OrderCreated):
        self.notification_service.send(event.user_email, "Змовлення успішно створене.")
