# src/common/providers.py
import os
from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.common.uow import SQLAlchemyUoW, UnitOfWork


class DBProvider(Provider):
    """Провайдер общей инфраструктуры БД"""

    @provide(scope=Scope.APP)
    def get_engine(self) -> AsyncEngine:
        """Создаёт движок БД (синглтон на всё приложение)"""
        # DSN берётся из переменных окружения
        database_url = os.getenv(
            "DATABASE_URL", "postgresql+asyncpg://admin:1234@localhost:5432/mydb"
        )
        engine = create_async_engine(
            database_url,
            echo=True,  # для разработки включить логирование запросов
        )
        return engine

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, engine: AsyncEngine
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Создаёт сессию БД на каждый запрос.

        ⚠️ Генератор с yield = автоматическое закрытие при выходе из REQUEST
        """
        async_session = async_sessionmaker(
            engine,
            expire_on_commit=False,  # важно для асинхронности
        )

        async with async_session() as session:
            print("[DB] 🗄️ Session opened")
            try:
                yield session
            finally:
                # Сессия закроется при выходе из контекста
                print("[DB] 🗄️ Session closed")

    @provide(scope=Scope.REQUEST)
    def get_uow(self, session: AsyncSession) -> UnitOfWork:
        """Создаёт Unit of Work из сессии"""
        return SQLAlchemyUoW(session)
