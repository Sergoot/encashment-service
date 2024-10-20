from pydantic import BaseModel


class Coords(BaseModel):
    lat: float
    long: float


class Capacity(BaseModel):
    current: int
    max: int


class AtmCapacity(BaseModel):
    priem: Capacity
    vidacha: Capacity


class AtmModel(BaseModel):
    id: int
    coords: Coords
    capacity: AtmCapacity

