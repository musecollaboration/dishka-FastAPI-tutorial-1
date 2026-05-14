# src/orders/infrastructure/models.py
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""

    pass


class OrderModel(Base):
    """SQLAlchemy модель заказа (только для БД!)"""

    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    customer_id: Mapped[UUID]
    status: Mapped[str]
