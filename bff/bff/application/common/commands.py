from dataclasses import dataclass


@dataclass
class ComputeRouteCommand:
    current_lat: float
    current_long: float
    radius: int # метры
