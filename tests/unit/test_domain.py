import pytest
from src.domain.factories.user_factory import UserFactory
from src.domain.factories.order_factory import OrderFactory
from src.domain.errors import DomainError
from unittest.mock import MagicMock


def test_user_factory_password_validation():
    mock_repo = MagicMock()
    mock_repo.get_by_username.return_value = None

    factory = UserFactory(user_repo=mock_repo)

    with pytest.raises(DomainError, match="Пароль занадто короткий"):
        factory.create(username="test", password="123")


def test_order_factory_empty_items():
    mock_order_repo = MagicMock()
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_id.return_value = True
    factory = OrderFactory(order_repo=mock_order_repo, user_repo=mock_user_repo)
    
    with pytest.raises(DomainError, match="Замовлення не може бути порожнім"):
        factory.create(user_id="1", items=[])
