from pydantic import BaseModel


class Coords(BaseModel):
    lat: float
    long: float


class Capacity(BaseModel):
    current: int
    max: int


class AtmCapacity(BaseModel):
    money_in: Capacity
    money_out: Capacity


class AtmCreate(BaseModel):
    osm_id: int
    coords: Coords
    capacity: AtmCapacity


class AtmModel(AtmCreate):
    id: int


class ChangeAtmCapacity(BaseModel):
    money_in_current: float
    money_out_current: float

class BaseResponse(BaseModel):
    status: bool
    message: str
    detail: str | None = None