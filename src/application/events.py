from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class OrderCreated:
    order_id: int
    user_email: str
    items: list[str]
    occurred_at: datetime
