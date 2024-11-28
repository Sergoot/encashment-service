from dataclasses import dataclass


@dataclass
class ComputeRouteQuery:
    current_lat: float
    current_long: float
    radius: int = 1000
