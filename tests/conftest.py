import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from flask_jwt_extended import create_access_token

from src.main import create_app
from src.config import TestConfig
from src.infrastructure.models import db, Base, UserEntity, ProductEntity

@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=TestConfig)
    from src.domain.factories.user_factory import UserFactory
    from src.infrastructure.repositories import PostgresUserRepository

    new_user_repo = PostgresUserRepository(db.session)
    app.user_factory = UserFactory(user_repo=new_user_repo)

    return app


@pytest.fixture
def client(app):
    """Create a test client with application context."""
    with app.app_context():
        with app.test_client() as client:
            yield client

@pytest.fixture
def db_session(app):
    """Clean database session for each test."""
    with app.app_context():
        db.session.query(UserEntity).delete()
        db.session.query(ProductEntity).delete()
        db.session.commit()

        connection = db.engine.connect()
        transaction = connection.begin()

        session = db.session
        session.remove()
        session.configure(bind=connection)

        yield session

        transaction.rollback()
        connection.close()
        session.remove()

@pytest.fixture
def auth_headers(app, db_session):
    """Create authentication headers and clean user."""
    with app.app_context():
        db_session.query(UserEntity).filter_by(username="testuser").delete()

        user = UserEntity(id="test-user-id", username="testuser", password_hash="hash")
        db_session.add(user)
        db_session.commit()

        token = create_access_token(identity="test-user-id")
        return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_uow():
    from unittest.mock import MagicMock
    return MagicMock()
