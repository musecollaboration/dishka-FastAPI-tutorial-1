# src/orders/domain/entities.py
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Order:
    """Бизнес-сущность заказа"""

    id: UUID
    customer_id: UUID
    status: str  # "pending", "paid", "shipped"

    @classmethod
    def create(cls, customer_id: UUID) -> "Order":
        """Фабричный метод создания нового заказа"""
        return cls(id=uuid4(), customer_id=customer_id, status="pending")

    def mark_as_paid(self) -> None:
        """Бизнес-правило: перевод заказа в статус 'paid'"""
        if self.status != "pending":
            raise ValueError(f"Cannot pay order in status '{self.status}'")
        self.status = "paid"
