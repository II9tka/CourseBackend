import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI

from settings import settings
from api.v1 import routers as api_v1
from container import Container

container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код до yield выполняется один раз на старте (инициализация ресурсов: БД, кэш, клиенты).

    sessionmanager = container.session_manager()
    sessionmanager.init(settings.database.get_database_url())

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

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.debug
    )
