from abc import ABC, abstractmethod

class AbstractNotificationService(ABC):
    @abstractmethod
    def send(self, user_email: str, message: str) -> None:
        pass
