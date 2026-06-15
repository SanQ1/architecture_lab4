from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    password: str
    email: str

@dataclass(frozen=True)
class CreateOrderCommand:
    items: list[str]
    user_id: str

@dataclass(frozen=True)
class AddProductCommand:
    name: str
    price: float

@dataclass(frozen=True)
class DeleteProductCommand:
    product_id: int

@dataclass(frozen=True)
class DeleteOrderCommand:
    order_id: int
