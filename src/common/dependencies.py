# src/common/dependencies.py
from dishka.integrations.fastapi import FromDishka

from orders.application.use_cases import CreateOrderUseCase, GetOrderUseCase
from orders.domain.interfaces import OrderRepository

# Алиасы для use cases модуля orders
CreateOrderUseCaseDep = FromDishka[CreateOrderUseCase]
GetOrderUseCaseDep = FromDishka[GetOrderUseCase]

# Алиасы для репозиториев
OrderRepoDep = FromDishka[OrderRepository]
