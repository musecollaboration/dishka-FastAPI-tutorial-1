# src/orders/domain/interfaces.py
from typing import Protocol, runtime_checkable
from uuid import UUID

from src.orders.domain.entities import Order


@runtime_checkable  # проверка в рантайме
class OrderRepository(Protocol):
    """Абстракция репозитория заказов (интерфейс порта)"""

    async def add(self, order: Order) -> None: ...
    async def get_by_id(self, order_id: UUID) -> Order | None: ...
