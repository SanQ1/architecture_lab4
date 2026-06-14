from dataclasses import dataclass
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from src.application.queries import GetUserByIdQuery, ListAllProductsQuery, LoginQuery
from src.infrastructure.models import UserEntity, ProductEntity, UserEntity
from src.domain.errors import DomainError

# --- Read Models ---
@dataclass(frozen=True)
class UserReadModel:
    id: str
    username: str

@dataclass(frozen=True)
class ProductReadModel:
    id: int
    name: str
    price: float

@dataclass(frozen=True)
class TokenReadModel:
    access_token: str


# --- Query Handlers ---
class LoginQueryHandler:
    def __init__(self, session):
        self.session = session

    def handle(self, query: LoginQuery) -> TokenReadModel:
        user = self.session.query(UserEntity).filter_by(username=query.username).first()
        
        if not user or not check_password_hash(user.password_hash, query.password):
            raise DomainError("Невірний логін або пароль")
            
        token = create_access_token(identity=str(user.id))
        return TokenReadModel(access_token=token)


class GetUserByIdQueryHandler:
    def __init__(self, session):
        self.session = session

    def handle(self, query: GetUserByIdQuery) -> UserReadModel | None:
        entity = self.session.get(UserEntity, query.user_id)
        if not entity:
            return None
            
        return UserReadModel(
            id=entity.id,
            username=entity.username
        )


class ListAllProductsQueryHandler:
    def __init__(self, session):
        self.session = session

    def handle(self, query: ListAllProductsQuery) -> list[ProductReadModel]:
        entities = self.session.query(ProductEntity).all()
        
        return [
            ProductReadModel(id=e.id, name=e.name, price=e.price)
            for e in entities
        ]
