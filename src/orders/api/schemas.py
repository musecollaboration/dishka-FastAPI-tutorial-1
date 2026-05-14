# src/orders/api/schemas.py
from pydantic import UUID4, BaseModel, Field


class OrderCreateSchema(BaseModel):
    """Схема для создания заказа (входные данные HTTP)"""  # ... означает обязательное поле

    customer_id: UUID4 = Field(..., description="ID покупателя")

    class Config:
        json_schema_extra = {
            "example": {"customer_id": "550e8400-e29b-41d4-a716-446655440000"}
        }


class OrderResponseSchema(BaseModel):
    """Схема ответа с данными заказа"""

    id: UUID4
    status: str

    class Config:
        from_attributes = True  # для работы с dataclass
