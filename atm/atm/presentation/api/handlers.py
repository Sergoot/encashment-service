from fastapi import APIRouter


router = APIRouter()


@router.get("")
async def get_computed_routes() -> dict:
    return {
        "atms": [
            {"id": 1, "location": [124.511, 2134.16]},
            {"id": 2, "location": [14.145, 612.24]},
            {"id": 3, "location": [51.154, 1441.15]},
        ]
    }