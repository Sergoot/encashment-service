from dataclasses import dataclass
from typing import Any


@dataclass
class ClosestBodyRequest:
    atms: list[Any]
    current_lat: float
    current_long: float
