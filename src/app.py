from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1 import routers as api_v1
from container import Container

container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код до yield выполняется один раз на старте (инициализация ресурсов: БД, кэш, клиенты).

    sessionmanager = container.session_manager()
    sessionmanager.init("postgresql+asyncpg://user:password@localhost:5433/backend_course")

    # --- startup: создаём таблицы один раз (идемпотентно) ---

    async with sessionmanager.connect() as connection:
        await sessionmanager.create_all(connection)

    try:
        yield

        # Код после yield выполняется при остановке (корректно закрываем соединения, пулы и т.д.).
    finally:
        # --- shutdown: корректно закрываем пул соединений ---
        await sessionmanager.close()


container.wire(
    modules=[
        "infrastructure.databases.postgresql.session",
        "api.v1.author.dependencies",
    ]
)

app = FastAPI(lifespan=lifespan)
app.include_router(api_v1.router)
