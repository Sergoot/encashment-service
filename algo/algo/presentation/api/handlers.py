from fastapi import APIRouter


router = APIRouter()


@router.post("")
async def compute(data: dict) -> dict:
    
    return {
        "routes": [
            [14.145, 612.24],
            [124.511, 2134.16],
            [51.154, 1441.15],
        ]
    }