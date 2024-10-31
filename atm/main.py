from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import init_db
from src.router import main_router

@asynccontextmanager
async def lifespan(app):
    await init_db()
    yield


app = FastAPI(
    debug=True,
    title="Сервис банкоматов города Москвы",
    version="0.1.0",
    lifespan=lifespan
)


app.include_router(main_router)
