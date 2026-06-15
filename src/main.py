import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from src.infrastructure.models import db
from src.presentation.controllers import api_bp
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.domain.factories.order_factory import OrderFactory
from src.domain.factories.user_factory import UserFactory
from src.infrastructure.repositories import PostgresUserRepository, PostgresOrderRepository
from src.infrastructure.notifications.email_service import EmailNotificationService
from src.application.events_handler import NotificationEventHandler
from src.infrastructure.event_bus import EventBus
from src.application.events import OrderCreated
from src.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'GjGISdgJSDHudhuBGBDuHDSUHbGUDIgRIHGEIldafJ-key')

    db.init_app(app)
    jwt = JWTManager(app)

    user_repo = PostgresUserRepository(session=db.session)
    order_repo = PostgresOrderRepository(session=db.session)
    notification_service = EmailNotificationService()

    user_factory = UserFactory(user_repo=user_repo)
    order_factory = OrderFactory(order_repo=order_repo, user_repo=user_repo)

    uow = SQLAlchemyUnitOfWork() 

    bus = EventBus()
    notification_handler = NotificationEventHandler(notification_service)
    bus.subscribe(OrderCreated, notification_handler.on_order_created)
    
    app.db = db
    app.uow = uow
    app.user_factory = user_factory
    app.order_factory = order_factory
    app.notification_service = notification_service
    app.event_bus = bus

    app.register_blueprint(api_bp, url_prefix='/api/v1')

    if not app.config.get("TESTING"):
        with app.app_context():
            db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
