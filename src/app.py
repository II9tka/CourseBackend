from fastapi import FastAPI

from api.v1 import routers as api_v1

app = FastAPI()
app.include_router(api_v1.router)
# app.mount("/api/v1", api_v1.router)
