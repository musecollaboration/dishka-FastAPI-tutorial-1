# src/orders/application/use_cases.py
from uuid import UUID

from src.common.uow import UnitOfWork  # интерфейс из общего модуля
from src.orders.application.dto import CreateOrderDTO
from src.orders.domain.entities import Order
from src.orders.domain.exceptions import OrderNotFoundError
from src.orders.domain.interfaces import OrderRepository


class CreateOrderUseCase:
    """Use case: создание нового заказа"""

    def __init__(
        self,
        repository: OrderRepository,  # ← зависит от абстракции!
        uow: UnitOfWork,
    ):
        self.repository = repository
        self.uow = uow

    async def execute(self, data: CreateOrderDTO) -> UUID:
        """
        Выполняет сценарий создания заказа.

        Возвращает ID созданного заказа.
        """
        # 1. Создаём сущность через фабричный метод (бизнес-правило)
        order = Order.create(data.customer_id)

        # 2. Unit of Work управляет транзакцией
        async with self.uow:
            # 3. Сохраняем через абстракцию репозитория
            await self.repository.add(order)
            # uow закоммитит при выходе из контекста, если нет ошибки

        # 4. Возвращаем результат
        return order.id


class GetOrderUseCase:
    """Use case: получение заказа по ID"""

    def __init__(self, repository: OrderRepository, uow: UnitOfWork):
        self.repository = repository
        self.uow = uow

    async def execute(self, order_id: UUID) -> Order:
        """Получает заказ или выбрасывает исключение"""
        async with self.uow:
            order = await self.repository.get_by_id(order_id)

        if order is None:
            raise OrderNotFoundError(order_id)

        return order
