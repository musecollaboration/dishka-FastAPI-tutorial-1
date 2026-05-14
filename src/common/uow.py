# src/common/uow.py
from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession


@runtime_checkable  # проверка в рантайме
class UnitOfWork(Protocol):
    """Абстракция паттерна Unit of Work (интерфейс)"""

    async def commit(self) -> None:
        """Фиксирует транзакцию"""
        pass

    async def rollback(self) -> None:
        """Откатывает транзакцию"""
        pass

    async def __aenter__(self):
        """Вход в контекст"""
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекста: commit или rollback"""
        pass


class SQLAlchemyUoW:
    """Реализация Unit of Work на SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> "SQLAlchemyUoW":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        При выходе из контекста:
        - если было исключение → rollback
        - иначе → commit
        """
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        # Сессия закроется автоматически при выходе из REQUEST-скоупа Dishka

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
