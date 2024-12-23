from typing import Any, Callable
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings
from .di import api_client_factory, compute_route_factory
from bff.presentation.api import root_router
from bff.application.common.interfaces import IComputeRoute


def as_dependency(dependency: Any) -> Callable:
    def dependency_factory() -> Any:
        return dependency
    
    return dependency_factory


def create_app(settings: Settings):
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    atm_client = api_client_factory(settings.atm_host, settings.atm_port)
    algo_client = api_client_factory(settings.algo_host, settings.algo_port)
    
    compute_route = compute_route_factory(atm_client, algo_client)
    
    app.dependency_overrides.update(
        {
            IComputeRoute: as_dependency(compute_route)
        }
    )
    
    app.include_router(root_router)
    return app


def app_factory():
    settings = Settings()
    return create_app(settings)
