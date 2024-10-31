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


class AtmCreate(BaseModel):
    coords: Coords
    capacity: AtmCapacity


class AtmModel(AtmCreate):
    id: int


class ChangeAtmCapacity(BaseModel):
    id: int
    priem: float
    vidacha: float

class BaseResponse(BaseModel):
    status: bool
    message: str
    detail: str | None = None