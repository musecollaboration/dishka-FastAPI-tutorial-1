# src/orders/domain/exceptions.py
from uuid import UUID


class OrderNotFoundError(Exception):
    """Заказ не найден"""

    def __init__(self, order_id: UUID):
        super().__init__(f"Order {order_id} not found")
