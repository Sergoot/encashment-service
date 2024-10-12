from fastapi import FastAPI


def create_app():
    app = FastAPI
    return app


def app_factory():
    return create_app()
