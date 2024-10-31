from typing import Any
from fastapi import APIRouter, Body


router = APIRouter()


@router.post("")
async def compute(data: list = Body(default_factory=list())) -> dict:
    
    return {
        "routes": [
            [14.145, 612.24],
            [124.511, 2134.16],
            [51.154, 1441.15],
        ]
    }
