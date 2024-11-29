from pydantic import BaseModel


class Coords(BaseModel):
    lat: float
    long: float


class Capacity(BaseModel):
    current: int
    max: int


class AtmCreate(BaseModel):
    osm_id: int
    coords: Coords
    capacity: Capacity


class AtmModel(AtmCreate):
    id: int


class ChangeAtmCapacity(BaseModel):
    money_current: float

class BaseResponse(BaseModel):
    status: bool
    message: str
    detail: str | None = None