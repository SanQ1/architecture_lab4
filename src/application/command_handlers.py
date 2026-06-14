from src.application.commands import (
    RegisterUserCommand,
    CreateOrderCommand,
    AddProductCommand,
    DeleteProductCommand,
    DeleteOrderCommand
)
from src.domain.models import Product
from src.infrastructure.models import UserEntity, ProductEntity, OrderEntity
from src.domain.errors import DomainError


class RegisterUserCommandHandler:
    def __init__(self, uow, factory):
        self.uow = uow
        self.factory = factory

    def handle(self, command: RegisterUserCommand) -> str:
        with self.uow:
            user = self.factory.create(
                username=command.username, 
                password=command.password
            )
            
            self.uow.users.add(user)
            self.uow.commit()
            return user.id


class CreateOrderCommandHandler:
    def __init__(self, uow, factory):
        self.uow = uow
        self.factory = factory

    def handle(self, command: CreateOrderCommand) -> int:
        with self.uow:
            order = self.factory.create(
                user_id=command.user_id, 
                items=command.items
            )
            
            self.uow.orders.add(order)
            self.uow.commit()
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
