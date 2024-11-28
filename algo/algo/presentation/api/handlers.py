from typing import Any
from fastapi import APIRouter, Body, HTTPException
import random

from .schemas import ClosestBodyRequest


router = APIRouter()


@router.post("")
async def compute(data: list = Body(default_factory=list())) -> dict:
    random.shuffle(data)
    return {
        "routes": [
            [atm["coords"]["lat"], atm["coords"]["long"]]
            for atm in data
        ]
    }


@router.post("/next")
async def compute(data: ClosestBodyRequest) -> Any:
    if data.atms:
        return data.atms[0]
    raise HTTPException(status_code=409, detail="No atms to be computed")
