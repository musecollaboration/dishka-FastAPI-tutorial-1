# FastAPI + Dishka: Чистая архитектура с Dependency Injection

> **Учебный проект** для демонстрации чистой архитектуры и современного подхода к разработке асинхронных API на Python

## 📋 Содержание

- [О проекте](#о-проекте)
- [Ключевые особенности](#ключевые-особенности)
- [Технологический стек](#технологический-стек)
- [Архитектура](#архитектура)
- [Структура проекта](#структура-проекта)
- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Основные концепции](#основные-концепции)
- [Примеры кода](#примеры-кода)
- [Обсуждение в коде](#обсуждение-в-коде)

## О проекте

Это учебный проект, который демонстрирует **профессиональный подход к разработке современных API-приложений** на Python. Проект реализует классическую архитектуру **Clean Architecture** с применением **Dependency Injection** через библиотеку Dishka.

Основной фокус:

- **Разделение ответственности** — четкое разделение кода на слои
- **Dependency Injection** — слабая связанность компонентов
- **Тестируемость** — легкое написание unit-тестов
- **Масштабируемость** — простое добавление новых модулей
- **Асинхронность** — полная поддержка async/await

## Ключевые особенности

**FastAPI** — современный, быстрый фреймворк с автоматической генерацией OpenAPI документации  
**Dishka** — легкая и мощная библиотека для управления зависимостями  
**SQLAlchemy 2.0** — асинхронная ORM с полной типизацией  
**PostgreSQL** — надежная реляционная база данных  
**Pydantic v2** — валидация данных и сериализация  
**Alembic** — управление миграциями базы данных  
**Poetry** — современный менеджер зависимостей  
**Docker Compose** — простая локальная разработка

## Технологический стек

| Компонент      | Версия  | Назначение                      |
| -------------- | ------- | ------------------------------- |
| **Python**     | ≥ 3.12  | Язык программирования           |
| **FastAPI**    | ≥ 0.136 | Веб-фреймворк для API           |
| **Uvicorn**    | ≥ 0.46  | ASGI-сервер                     |
| **SQLAlchemy** | ≥ 2.0   | ORM, работа с БД                |
| **asyncpg**    | ≥ 0.31  | Асинхронный драйвер PostgreSQL  |
| **Pydantic**   | ≥ 2.13  | Валидация и сериализация данных |
| **Dishka**     | ≥ 1.10  | Dependency Injection контейнер  |
| **Alembic**    | ≥ 1.18  | Миграции БД                     |
| **PostgreSQL** | 17      | Реляционная база данных         |

## Архитектура

Проект использует **Clean Architecture** — архитектурный стиль, который оптимально разделяет ответственность между слоями.

### Слои приложения

```
┌─────────────────────────────────────────┐
│         API Layer (FastAPI)             │ ← HTTP, роутеры, валидация Pydantic
├─────────────────────────────────────────┤
│    Application Layer (Use Cases)        │ ← Бизнес-логика, координация
├─────────────────────────────────────────┤
│      Domain Layer (Entities)            │ ← Правила бизнеса, исключения
├─────────────────────────────────────────┤
│   Infrastructure Layer (Repositories)   │ ← БД, внешние сервисы
└─────────────────────────────────────────┘
```

### Преимущества такого разделения

| Слой               | Описание                                | Зависит от               |
| ------------------ | --------------------------------------- | ------------------------ |
| **API**            | Преобразование HTTP в доменные сущности | Приложение               |
| **Application**    | Use cases, координация, DTO             | Domain + Infrastructure  |
| **Domain**         | Правила бизнеса, сущности, исключения   | Ничего                   |
| **Infrastructure** | Реализация репозиториев, подключение БД | Ничего (внешние сервисы) |

**Ключевой принцип:** Внутренние слои не зависят от внешних → легко менять реализацию БД, фреймворка и т.д.

## Структура проекта

```
dishka-fastapi-tutorial-1/
│
├── src/                              # Исходный код приложения
│   ├── main.py                         # Точка входа приложения
│   ├── ioc.py                          # Composition Root (DI контейнер)
│   │
│   ├── common/                       # Общая инфраструктура
│   │   ├── providers.py                # Провайдеры БД и UoW
│   │   ├── dependencies.py             # Общие зависимости
│   │   └── uow.py                      # Unit of Work паттерн
│   │
│   └── orders/                       # Модуль "Заказы" (пример)
│       ├── api/                        # HTTP слой
│       │   ├── routes.py               # FastAPI роутеры и эндпоинты
│       │   └── schemas.py              # Pydantic схемы
│       │
│       ├── application/              # Прикладной слой
│       │   ├── use_cases.py            # Бизнес-логика (use cases)
│       │   ├── dto.py                  # Data Transfer Objects
│       │   └── providers.py            # Провайдеры зависимостей модуля
│       │
│       ├── domain/                   # Доменный слой
│       │   ├── entities.py             # Доменные сущности
│       │   ├── exceptions.py           # Доменные исключения
│       │   └── interfaces.py           # Интерфейсы репозиториев
│       │
│       └── infrastructure/           # Инфраструктурный слой
│           ├── models.py               # SQLAlchemy модели
│           ├── adapters.py             # Адаптеры для БД
│           ├── mappers.py              # Преобразования Entity ↔ Model
│           └── providers.py            # Провайдеры инфраструктуры
│
├── tests/                            # Тесты
│   ├── conftest.py                     # Конфигурация pytest
│   └── orders/
│       ├── test_api.py                 # Тесты API
│       └── test_use_cases.py           # Тесты бизнес-логики
│
├── migrations/                       # Alembic миграции БД
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── docker-compose.yml                # Docker для PostgreSQL
├── alembic.ini                       # Конфигурация Alembic
├── pyproject.toml                    # Конфигурация Poetry
├── README.md                         # README
└── .env                              # Переменные окружения (локально)
```

## Установка

### Требования

- **Python** ≥ 3.12
- **Poetry** ≥ 1.7
- **Docker & Docker Compose** (для PostgreSQL)

### Пошаговая установка

#### 1. Клонируем репозиторий

```bash
git clone <repository-url>
cd dishka-fastapi-tutorial-1
```

#### 2. Создаем виртуальное окружение

```bash
# Poetry автоматически создаст .venv в директории проекта
poetry config virtualenvs.in-project true
```

#### 3. Устанавливаем зависимости

```bash
poetry install
```

Это установит все зависимости из `pyproject.toml`:

- FastAPI
- SQLAlchemy
- Dishka
- Alembic
- И другие...

#### 4. Создаем файл конфигурации .env

```bash
# Скопируем пример
cp .env.example .env
```

или создадим вручную:

```bash
cat > .env << EOF
# Database
DATABASE_URL=postgresql+asyncpg://admin:1234@localhost:5432/mydb
POSTGRES_DB=mydb
POSTGRES_USER=admin
POSTGRES_PASSWORD=1234
EOF
```

#### 5. Запускаем PostgreSQL

```bash
docker-compose up -d
```

Это запустит PostgreSQL в контейнере.  
Проверить статус:

```bash
docker-compose ps
```

#### 6. Применяем миграции

```bash
poetry run alembic upgrade head
```

Это создаст все необходимые таблицы в БД.

## Быстрый старт

### Запуск приложения в режиме разработки

```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Приложение будет доступно по адресу: **http://localhost:8000**

### Просмотр документации API

FastAPI автоматически генерирует интерактивную документацию:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Примеры запросов

#### Создать заказ

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "550e8400-e29b-41d4-a716-446655440000"}'
```

**Ответ:**

```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "status": "pending"
}
```

#### Получить заказ

```bash
curl "http://localhost:8000/orders/f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

**Ответ:**

```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "status": "pending"
}
```

## Разработка

### Структура разработки

Проект использует **асинхронное программирование** (async/await) на протяжении всей цепочки:

```
FastAPI (async) → Use Case (async) → Repository (async) → SQLAlchemy (async)
```

### Добавление нового модуля

Чтобы добавить новый модуль (например, "Платежи"):

#### 1. Создайте структуру директорий

```bash
mkdir -p src/payments/{api,application,domain,infrastructure}
touch src/payments/__init__.py
touch src/payments/{api,application,domain,infrastructure}/__init__.py
```

#### 2. Создайте модели и сущности

```python
# src/payments/domain/entities.py
from uuid import UUID
from dataclasses import dataclass
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Payment:
    id: UUID
    order_id: UUID
    amount: float
    status: PaymentStatus
```

#### 3. Создайте use case

```python
# src/payments/application/use_cases.py
from uuid import UUID
from src.payments.domain.entities import Payment

class ProcessPaymentUseCase:
    def __init__(self, repository):
        self.repository = repository

    async def execute(self, order_id: UUID, amount: float) -> UUID:
        payment = Payment(
            id=UUID(...),
            order_id=order_id,
            amount=amount,
            status="pending"
        )
        await self.repository.add(payment)
        return payment.id
```

#### 4. Создайте API роуты

```python
# src/payments/api/routes.py
from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import inject, FromDishka
from src.payments.application.use_cases import ProcessPaymentUseCase

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/")
@inject
async def process_payment(
    use_case: FromDishka[ProcessPaymentUseCase],
):
    # ...
    pass
```

#### 5. Зарегистрируйте в контейнере DI

```python
# src/ioc.py
from src.payments.infrastructure.providers import PaymentProvider

def get_container():
    return make_async_container(
        DBProvider(),
        OrderProvider(),
        PaymentProvider(),  # ← новый модуль
    )
```

### Линтинг и форматирование

```bash
# Проверка стиля кода
poetry run pylint src/

# Форматирование кода (если установлен black)
poetry run black src/
```

## Тестирование

### Запуск тестов

```bash
# Все тесты
poetry run pytest

# С выводом покрытия
poetry run pytest --cov=src

# Только тесты определенного модуля
poetry run pytest tests/orders/

# С подробным выводом
poetry run pytest -v

# Останавливаться на первой ошибке
poetry run pytest -x
```

### Структура тестов

Тесты располагаются в директории `tests/` с аналогичной структурой как в `src/`:

```python
# tests/orders/test_use_cases.py
import pytest
from uuid import UUID
from unittest.mock import AsyncMock

from src.orders.application.use_cases import CreateOrderUseCase
from src.orders.application.dto import CreateOrderDTO


@pytest.mark.asyncio
async def test_create_order():
    # Arrange
    mock_repository = AsyncMock()
    use_case = CreateOrderUseCase(mock_repository)
    dto = CreateOrderDTO(customer_id=UUID('550e8400-e29b-41d4-a716-446655440000'))

    # Act
    order_id = await use_case.execute(dto)

    # Assert
    assert order_id is not None
    mock_repository.add.assert_called_once()
```

### pytest fixtures

В `tests/conftest.py` определены общие fixtures:

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session
```

## Основные концепции

### 1. Dependency Injection (DI)

**Что это?** Паттерн, при котором зависимости объекта поступают извне (не создаются самим объектом).

**Пример без DI:**

```python
class OrderUseCase:
    def __init__(self):
        self.repository = OrderRepository()  # ❌ Сложно тестировать
```

**С Dishka (DI):**

```python
class OrderUseCase:
    def __init__(self, repository: OrderRepository):  # ✅ Легко подменять
        self.repository = repository
```

Dishka автоматически создает экземпляры и подставляет их.

### 2. Unit of Work (UoW)

**Паттерн**, который управляет набором репозиториев и одной транзакцией БД.

```python
# src/common/uow.py
class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.orders = OrderRepository(session)
        self.payments = PaymentRepository(session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
```

**Использование:**

```python
async def process_order(uow: UnitOfWork, order_id: UUID):
    try:
        order = await uow.orders.get(order_id)
        payment = await uow.payments.create(order)
        await uow.commit()  # Все или ничего!
    except Exception:
        await uow.rollback()  # Откатываем изменения
        raise
```

### 3. DTO (Data Transfer Object)

**Зачем нужны?** Разделяют слои приложения, преобразуют данные между слоями.

```python
# API слой (Pydantic)
class OrderCreateSchema(BaseModel):
    customer_id: UUID

# Application слой (обычный class)
@dataclass
class CreateOrderDTO:
    customer_id: UUID

# Domain слой (сущность)
@dataclass
class Order:
    id: UUID
    customer_id: UUID
    status: str

# Преобразование в маршруте
@router.post("/orders/")
async def create_order(
    schema: OrderCreateSchema,  # ← от клиента
    use_case: FromDishka[CreateOrderUseCase],
):
    dto = CreateOrderDTO(**schema.model_dump())  # ← преобразуем
    order_id = await use_case.execute(dto)
    return {"id": order_id}
```

### 4. Protocol (Структурная типизация)

**Что это?** Protocol из модуля `typing` — это способ определить интерфейс **без наследования**.

**Традиционный подход (ABC):**

```python
from abc import ABC, abstractmethod

class OrderRepository(ABC):  # ← явное наследование
    @abstractmethod
    async def save(self, order: Order) -> Order: ...
```

**Современный подход (Protocol):**

```python
from typing import Protocol

class OrderRepository(Protocol):  # ← просто описываем контракт
    async def add(self, order: Order) -> None: ...
    async def get_by_id(self, order_id: UUID) -> Order | None: ...
```

**Преимущества Protocol:**

- ✅ Нет необходимости в явном наследовании
- ✅ Любой класс с нужными методами автоматически соответствует Protocol
- ✅ Лучшая поддержка type checking в IDE
- ✅ Проще для тестирования (легче создавать моки)

### 5. Repositories

**Паттерн для работы с БД**, который скрывает детали реализации. Используется **Protocol** для определения интерфейса без наследования.

```python
# src/orders/domain/interfaces.py
from typing import Protocol
from uuid import UUID
from src.orders.domain.entities import Order

class OrderRepository(Protocol):
    """Протокол (интерфейс) репозитория заказов"""
    async def add(self, order: Order) -> None: ...
    async def get_by_id(self, order_id: UUID) -> Order | None: ...

# src/orders/infrastructure/adapters.py
from sqlalchemy.ext.asyncio import AsyncSession
from src.orders.domain.entities import Order
from src.orders.domain.interfaces import OrderRepository
from src.orders.infrastructure.models import OrderModel

class SQLAlchemyOrderRepository:
    """Реализация репозитория через SQLAlchemy"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, order: Order) -> None:
        """Сохраняет заказ в БД"""
        model = OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status,
        )
        self.session.add(model)
        await self.session.flush()

    async def get_by_id(self, order_id: UUID) -> Order | None:
        """Получает заказ по ID"""
        model = await self.session.get(OrderModel, order_id)
        if not model:
            return None
        return self._map_to_entity(model)

    def _map_to_entity(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            status=model.status,
        )
```

### 6. Scopes в Dishka

Dishka поддерживает разные **жизненные циклы** зависимостей:

| Scope       | Описание                             | Пример               |
| ----------- | ------------------------------------ | -------------------- |
| `APP`       | Создается один раз при запуске       | Пул подключений к БД |
| `REQUEST`   | Создается на каждый HTTP запрос      | Session БД           |
| `EXECUTION` | Создается для каждого вызова функции | Логгер запроса       |

```python
# src/common/providers.py
from dishka import provide, Scope

class DBProvider:
    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncEngine:
        # Создается один раз и переиспользуется
        return create_async_engine(DATABASE_URL)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, engine: AsyncEngine
    ) -> AsyncSession:
        # Создается на каждый запрос
        async with AsyncSession(engine) as session:
            yield session
```

## Примеры кода

### Создание заказа (полный цикл)

#### 1. Маршрут (API слой)

```python
# src/orders/api/routes.py
from fastapi import APIRouter
from dishka.integrations.fastapi import inject, FromDishka

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponseSchema)
@inject
async def create_order(
    schema: OrderCreateSchema,
    use_case: FromDishka[CreateOrderUseCase],
) -> OrderResponseSchema:
    # Преобразуем Pydantic-схему в DTO
    dto = CreateOrderDTO(customer_id=schema.customer_id)

    # Выполняем use case
    order_id = await use_case.execute(dto)

    # Возвращаем результат
    return OrderResponseSchema(id=order_id, status="pending")
```

#### 2. Use Case (Application слой)

```python
# src/orders/application/use_cases.py
from uuid import uuid4
from src.orders.application.dto import CreateOrderDTO
from src.orders.domain.entities import Order
from src.orders.domain.interfaces import OrderRepository  # Protocol

class CreateOrderUseCase:
    """Use case для создания заказа.

    Зависит от Protocol (интерфейса) OrderRepository,
    что позволяет использовать любую реализацию.
    """
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def execute(self, dto: CreateOrderDTO) -> UUID:
        # Создаем доменную сущность
        order = Order(
            id=uuid4(),
            customer_id=dto.customer_id,
            status="pending",
        )

        # Сохраняем через репозиторий (работает с Protocol)
        await self.repository.add(order)

        return order.id
```

#### 3. Репозиторий (Infrastructure слой)

```python
# src/orders/infrastructure/adapters.py
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.orders.domain.entities import Order
from src.orders.domain.interfaces import OrderRepository  # Protocol
from src.orders.infrastructure.models import OrderModel

class SQLAlchemyOrderRepository:
    """Конкретная реализация репозитория через SQLAlchemy.

    Автоматически соответствует Protocol благодаря структурной типизации.
    Не нужно наследоваться от OrderRepository!
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, order: Order) -> None:
        # Преобразуем сущность в модель БД
        model = self._map_to_model(order)
        self.session.add(model)
        await self.session.flush()

    async def get_by_id(self, order_id: UUID) -> Order | None:
        model = await self.session.get(OrderModel, order_id)
        if not model:
            return None
        return self._map_to_entity(model)

    def _map_to_model(self, order: Order) -> OrderModel:
        return OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status,
        )

    def _map_to_entity(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            status=model.status,
        )
```

#### 4. Модель БД (Domain слой)

```python
# src/orders/infrastructure/models.py
from uuid import UUID
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from src.common.models import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    customer_id = Column(PostgresUUID(as_uuid=True), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
```

### Тестирование Use Case

```python
# tests/orders/test_use_cases.py
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from src.orders.application.use_cases import CreateOrderUseCase
from src.orders.application.dto import CreateOrderDTO
from src.orders.domain.entities import Order


@pytest.mark.asyncio
async def test_create_order_success():
    """Тест успешного создания заказа"""
    # Arrange (подготовка)
    mock_repository = AsyncMock()
    use_case = CreateOrderUseCase(mock_repository)

    customer_id = uuid4()
    dto = CreateOrderDTO(customer_id=customer_id)

    # Act (действие)
    result = await use_case.execute(dto)

    # Assert (проверка)
    assert isinstance(result, type(uuid4()))
    mock_repository.add.assert_called_once()

    # Проверяем, что был вызван add с правильным объектом
    called_order = mock_repository.add.call_args[0][0]
    assert called_order.customer_id == customer_id
    assert called_order.status == "pending"
```

## Обсуждение в коде

Проект содержит **подробные комментарии** для обучения. Найти их можно в основных файлах:

- `src/main.py` — управление жизненным циклом приложения
- `src/ioc.py` — как работает контейнер DI
- `src/orders/api/routes.py` — как использовать Dishka в FastAPI
- `src/orders/application/use_cases.py` — структура use case
- `src/common/uow.py` — паттерн Unit of Work
- `tests/conftest.py` — как писать тесты

Каждый раздел кода содержит подробные объяснения на русском языке.

## Управление базой данных

### Создание миграции

```bash
# Создаем новую миграцию с автогенерацией
poetry run alembic revision --autogenerate -m "Add payment table"
```

Это создаст новый файл в `migrations/versions/`.

### Применение миграций

```bash
# Применить все миграции
poetry run alembic upgrade head

# Откатить на одну версию назад
poetry run alembic downgrade -1

# Посмотреть текущую версию
poetry run alembic current
```

### История миграций

```bash
# Посмотреть историю
poetry run alembic history --verbose
```

## Полезные команды

```bash
# Активировать виртуальное окружение
source .venv/bin/activate

# Запустить приложение
poetry run uvicorn src.main:app --reload

# Запустить тесты
poetry run pytest -v

# Проверить синтаксис
poetry run pylint src/

# Установить новый пакет
poetry add <package-name>

# Обновить зависимости
poetry update

# Остановить PostgreSQL
docker-compose down

# Посмотреть логи PostgreSQL
docker-compose logs postgres
```

## Часто задаваемые вопросы

### Q: Почему нужна чистая архитектура?

**A:** Чистая архитектура позволяет:

- Легко менять детали реализации (БД, фреймворк)
- Писать unit-тесты без мокирования всей системы
- Масштабировать проект добавляя новые модули
- Договориться о коде в команде

### Q: Что такое Composition Root?

**A:** Это `src/ioc.py` — единственное место, где известны все зависимости и их конкретные реализации. Остальной код работает с интерфейсами.

### Q: Зачем нужны DTO?

**A:** DTO отделяют слои приложения:

- API слой работает с `Schema` (Pydantic)
- Application слой работает с `DTO`
- Domain слой работает с `Entity`

Это позволяет менять API без влияния на бизнес-логику.

### Q: Как добавить новый модуль?

**A:** Скопируйте структуру `src/orders/` в новую директорию, обновите `src/ioc.py`, добавьте провайдер.

### Q: Что такое Protocol и почему он лучше ABC?

**A:** Protocol — это способ определить интерфейс без явного наследования:

| Аспект                    | ABC                               | Protocol                   |
| ------------------------- | --------------------------------- | -------------------------- |
| **Наследование**          | ✅ Требует явного наследования    | ❌ Не требует наследования |
| **Методы**                | Помечаются `@abstractmethod`      | Просто описываются         |
| **Type Checking**         | Работает, но менее гибко          | ✅ Работает лучше в IDE    |
| **Тестирование**          | Нужно создавать полные реализации | ✅ Легче мокировать        |
| **Структурная типизация** | ❌ Не поддерживается              | ✅ Поддерживается          |

Protocol используется в этом проекте для определения интерфейсов репозиториев без создания пустых базовых классов.

### Q: Что делать при ошибке миграций?

**A:**

```bash
# Если миграции не применяются
docker-compose down -v  # Удаляем БД с данными
docker-compose up -d    # Запускаем новую БД
poetry run alembic upgrade head  # Применяем миграции
```

## Дополнительные ресурсы

- [Документация FastAPI](https://fastapi.tiangolo.com/ru/)
- [Документация Dishka](https://dishka.readthedocs.io/)
- [Документация SQLAlchemy](https://docs.sqlalchemy.org/)
- [Clean Architecture на Python](https://stepik.org/course/276482/promo)

## Лицензия

MIT License — используйте свободно в обучающих целях.

---

> 💡 **Совет для учащихся:** Не просто читайте код, но и изменяйте его! Добавьте новый модуль, создайте миграцию, напишите тесты. Только через практику вы поймете эти концепции.
