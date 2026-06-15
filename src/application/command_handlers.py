from src.application.commands import (
    RegisterUserCommand,
    CreateOrderCommand,
    AddProductCommand,
    DeleteProductCommand,
    DeleteOrderCommand
)
from src.domain.models import Product
from src.domain.errors import DomainError
from src.application.notifications.abstract_notification import AbstractNotificationService
from src.application.events import OrderCreated
from datetime import datetime


class RegisterUserCommandHandler:
    def __init__(self, uow, factory, notification_service: AbstractNotificationService):
        self.uow = uow
        self.factory = factory
        self.notification_service = notification_service

    def handle(self, command: RegisterUserCommand) -> str:
        with self.uow:
            user = self.factory.create(
                username=command.username, 
                password=command.password,
                email=command.email
            )
            
            self.uow.users.add(user)
            self.uow.commit()

            self.notification_service.send(user.email, "Користувача зареєстровано.")
            print("Користувача створено")

            return user.id


class CreateOrderCommandHandler:
    def __init__(self, uow, factory, event_bus):
        self.uow = uow
        self.factory = factory
        self.event_bus = event_bus

    def handle(self, command: CreateOrderCommand) -> int:
        with self.uow:
            user = self.uow.users.get_by_id(command.user_id)

            order = self.factory.create(
                user_id=command.user_id, 
                items=command.items
            )
            
            self.uow.orders.add(order)
            self.uow.commit()

            self.event_bus.publish(OrderCreated(
                order_id=order.id,
                user_email=user.email,
                items=order.items,
                occurred_at=datetime.utcnow()
            ))

            print("Замовлення створено")
            return order.id


class AddProductCommandHandler:
    def __init__(self, uow):
        self.uow = uow

    def handle(self, command: AddProductCommand) -> int:
        with self.uow:
            product = Product(name=command.name, price=command.price)
            
            self.uow.products.add(product)
            self.uow.commit()
            return product.id


class DeleteProductCommandHandler:
    def __init__(self, uow):
        self.uow = uow

    def handle(self, command: DeleteProductCommand) -> None:
        with self.uow:
            self.uow.products.delete(command.product_id)
            self.uow.commit()


class DeleteOrderCommandHandler:
    def __init__(self, uow):
        self.uow = uow

    def handle(self, command: DeleteOrderCommand) -> None:
        with self.uow:
            self.uow.products.delete(command.order_id)
            self.uow.commit()
