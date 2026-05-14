# src/main.py
"""
Точка входа в приложение.
"""

from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.ioc import get_container
from src.orders.api.routes import router as orders_router

# from auth.api.routes import router as auth_router
# from billing.api.routes import router as billing_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.

    Здесь можно закрыть контейнер при остановке приложения,
    чтобы выполнилась финализация APP-скоупа.
    """
    # Приложение запускается
    yield
    # Приложение останавливается → закрываем контейнер
    await app.state.dishka_container.close()
    print("🔚 Container closed, APP-scoped dependencies finalized")


# Создаём приложение с lifespan
app = FastAPI(
    title="Clean Architecture with Dishka",
    description="Пример интеграции Dishka + FastAPI + Clean Architecture",
    version="1.0.0",
    lifespan=lifespan,
)

# Подключаем роутеры модулей
app.include_router(orders_router)
# app.include_router(auth_router)
# app.include_router(billing_router)

# Создаём контейнер и подключаем Dishka к FastAPI
container = get_container()
setup_dishka(container, app)

# ─────────────────────────────────────────────────────
# Health check эндпоинт (без зависимостей)
# ─────────────────────────────────────────────────────


@app.get("/health")
async def health_check():
    """Проверка работоспособности приложения"""
    return {"status": "ok"}


# ─────────────────────────────────────────────────────
# Точка входа для uvicorn
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",  # формат: "файл:переменная_приложения"
        host="0.0.0.0",
        port=8000,
        reload=True,  # авто-перезагрузка при разработке
    )
