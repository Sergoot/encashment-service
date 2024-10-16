from pydantic import BaseModel


class AtmModel(BaseModel):
    id: int
    lat: float
    long: float
    balance: int
