# src/orders/infrastructure/adapters.py
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.domain.entities import Order as OrderEntity
from src.orders.infrastructure.mappers import OrderMapper
from src.orders.infrastructure.models import OrderModel


class SQLOrderRepository:
    """Реализация репозитория на SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, order: OrderEntity) -> None:
        """Сохраняет новый заказ"""
        # Маппинг: сущность → модель БД
        model = OrderMapper.to_model(order)
        self.session.add(model)
        # Не делаем commit здесь — это задача Unit of Work

    async def get_by_id(self, order_id: UUID) -> OrderEntity | None:
        """Получает заказ по ID"""
        result = await self.session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        model = result.scalar_one_or_none()

        if model:
            # Маппинг: модель БД → сущность
            return OrderMapper.to_entity(model)
        return None
