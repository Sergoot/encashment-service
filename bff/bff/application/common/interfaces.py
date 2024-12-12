import abc
from dataclasses import dataclass
from typing import Any, Protocol

from .commands import ComputeRouteCommand


class ApiClient(Protocol):
    async def get(self, url: str, query_data: dict | None = None) -> dict | list:
        pass
    
    async def post(self, url: str, data: dict) -> dict:
        pass

    async def patch(self, url: str, data: dict) -> dict:
        pass
    

@dataclass
class RouteResponse:
    next_step: Any


class IComputeRoute(abc.ABC):
    async def execute(self, command: ComputeRouteCommand) -> RouteResponse:
        ...