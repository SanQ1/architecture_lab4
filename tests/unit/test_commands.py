import pytest
from unittest.mock import MagicMock, PropertyMock
from src.application.commands import RegisterUserCommand, CreateOrderCommand
from src.application.command_handlers import RegisterUserCommandHandler, CreateOrderCommandHandler
from src.domain.models import User, Order

class FakeUserRepository:
    def __init__(self): self.users = {}
    def add(self, user): self.users[user.username] = user
    def get_by_username(self, username): return self.users.get(username)

class FakeOrderRepository:
    def __init__(self): self.orders = []
    def add(self, order): self.orders.append(order)


def test_register_user_handler():
    repo = FakeUserRepository()
    uow = MagicMock()
    uow.users = repo
    factory = MagicMock()

    user = User(id="uid-1", username="testuser", password_hash="hash")
    factory.create.return_value = user

    handler = RegisterUserCommandHandler(uow=uow, factory=factory)
    cmd = RegisterUserCommand(username="testuser", password="password123")

    user_id = handler.handle(cmd)

    assert user_id == "uid-1"
    assert repo.get_by_username("testuser") == user
    uow.commit.assert_called_once()

def test_create_order_handler():
    order_repo = FakeOrderRepository()
    user_repo = FakeUserRepository()
    uow = MagicMock()
    uow.orders = order_repo
    uow.users = user_repo
    
    factory = MagicMock()
    order = Order(user_id="u1", items=["Mouse"])
    factory.create_order.return_value = order
    
    handler = CreateOrderCommandHandler(uow=uow, factory=factory)
    cmd = CreateOrderCommand(user_id="u1", items=["Mouse"])
    
    order_id = handler.handle(cmd)
    
    assert len(order_repo.orders) == 1
    uow.commit.assert_called_once()
