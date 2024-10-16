from fastapi import FastAPI
from atm.src.router import main_router

app = FastAPI(
    debug=True,
    title="Сервис банкоматов города Москвы",
    version="0.1.0"
)

app.include_router(main_router)
