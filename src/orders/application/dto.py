# src/orders/application/dto.py
from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateOrderDTO:
    """DTO для создания заказа (входные данные use case)"""

    customer_id: UUID
