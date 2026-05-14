# src/orders/api/routes.py
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.orders.api.schemas import OrderCreateSchema, OrderResponseSchema
from src.orders.application.dto import CreateOrderDTO
from src.orders.application.use_cases import CreateOrderUseCase, GetOrderUseCase
from src.orders.domain.exceptions import OrderNotFoundError

# ─────────────────────────────────────────────────────
# Алиасы для зависимостей (улучшают читаемость)
# ─────────────────────────────────────────────────────
CreateOrderUseCaseDep = FromDishka[CreateOrderUseCase]
GetOrderUseCaseDep = FromDishka[GetOrderUseCase]

# ─────────────────────────────────────────────────────
# Роутер модуля
# ─────────────────────────────────────────────────────
router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED
)
@inject  # ← включаем обработку параметров Dishka
async def create_order(
    schema: OrderCreateSchema,  # ← Pydantic: FastAPI распарсит body
    use_case: CreateOrderUseCaseDep,  # ← Dishka: внедрит use case
) -> OrderResponseSchema:
    """Создаёт новый заказ"""
    # 1. Преобразуем Pydantic-схему в DTO (граница слоёв)
    dto = CreateOrderDTO(customer_id=schema.customer_id)

    # 2. Выполняем use case (бизнес-логика)
    order_id = await use_case.execute(dto)

    # 3. Возвращаем ответ (Pydantic-схема)
    return OrderResponseSchema(id=order_id, status="pending")


@router.get("/{order_id}", response_model=OrderResponseSchema)
@inject
async def get_order(
    order_id: UUID,  # ← FastAPI: распарсит из path
    use_case: GetOrderUseCaseDep,  # ← Dishka: внедрит use case
) -> OrderResponseSchema:
    """Получает заказ по ID"""
    try:
        # Выполняем use case
        order = await use_case.execute(order_id)
        return OrderResponseSchema(id=order.id, status=order.status)

    except OrderNotFoundError:
        # Преобразуем доменное исключение в HTTP-ответ
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found"
        )
