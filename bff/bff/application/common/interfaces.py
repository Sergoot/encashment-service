import abc
from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias

from .commands import ComputeRouteCommand


class ATMClient(Protocol):
    async def get_atms(self, query_data: dict[str, Any]) -> ...:
        pass


Routes: TypeAlias = list[list[float]]


class AlgoClient(Protocol):
    async def get_atms(self, query_data: dict[str, Any]) -> Routes:
        pass


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