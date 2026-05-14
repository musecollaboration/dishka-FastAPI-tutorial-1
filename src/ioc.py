# src/ioc.py
"""
Composition Root — единственное место в приложении,
где известны все конкретные реализации зависимостей.
"""

from dishka import make_async_container

from src.common.providers import DBProvider
from src.orders.infrastructure.providers import OrderProvider

# Здесь можно добавить другие модули:
# from auth.infrastructure.providers import AuthProvider
# from billing.infrastructure.providers import BillingProvider


def get_container():
    """
    Создаёт и возвращает асинхронный контейнер.

    Все провайдеры собираются здесь.
    """
    return make_async_container(
        DBProvider(),  # общая инфраструктура
        OrderProvider(),  # модуль заказов
        # AuthProvider(),          # модуль авторизации
        # BillingProvider(),       # модуль платежей
    )
