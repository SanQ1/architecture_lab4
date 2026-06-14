from dataclasses import dataclass

@dataclass(frozen=True)
class GetUserByIdQuery:
    user_id: str

@dataclass(frozen=True)
class ListAllProductsQuery:
    pass

@dataclass(frozen=True)
class LoginQuery:
    username: str
    password: str
