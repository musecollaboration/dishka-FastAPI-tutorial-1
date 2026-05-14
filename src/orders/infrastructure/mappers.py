# src/orders/infrastructure/mappers.py

from src.orders.domain.entities import Order
from src.orders.infrastructure.models import OrderModel


class OrderMapper:
    """Маппер: преобразует между моделью БД и доменной сущностью"""

    @staticmethod
    def to_entity(model: OrderModel) -> Order:
        """Из модели БД → в доменную сущность"""
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            status=model.status,
        )

    @staticmethod
    def to_model(entity: Order) -> OrderModel:
        """Из доменной сущности → в модель БД"""
        return OrderModel(
            id=entity.id,
            customer_id=entity.customer_id,
            status=entity.status,
        )
