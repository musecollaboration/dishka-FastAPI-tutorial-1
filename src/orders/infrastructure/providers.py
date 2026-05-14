# src/orders/infrastructure/providers.py
from dishka import Provider, Scope, alias, provide

from src.orders.application.use_cases import CreateOrderUseCase, GetOrderUseCase
from src.orders.domain.interfaces import OrderRepository
from src.orders.infrastructure.adapters import SQLOrderRepository


class OrderProvider(Provider):
    """Провайдер модуля заказов"""

    # 1. Регистрируем реализацию репозитория
    _sql_repo = provide(SQLOrderRepository, scope=Scope.REQUEST)

    # 2. Связываем интерфейс с реализацией через alias
    # Теперь при запросе OrderRepository будет возвращён SQLOrderRepository
    order_repo = alias(source=SQLOrderRepository, provides=OrderRepository)

    # 3. Регистрируем use cases; их зависимости будут внедрены автоматически
    create_order_uc = provide(CreateOrderUseCase, scope=Scope.REQUEST)
    get_order_uc = provide(GetOrderUseCase, scope=Scope.REQUEST)
