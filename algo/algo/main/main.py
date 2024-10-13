from fastapi import FastAPI

from algo.presentation.api import root_router


def create_app():
    app = FastAPI()
    app.include_router(root_router)
    
    return app


def app_factory():
    return create_app()
