from typing import Any
from fastapi import APIRouter, Body
import random

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

