from fastapi import APIRouter, Depends

from bff.application.common.interfaces import IComputeRoute, RouteResponse
from bff.application.common.commands import ComputeRouteCommand
from bff.presentation.schemas.requests import ComputeRouteQuery

router = APIRouter()



@router.get("/", response_model=RouteResponse)
async def get_computed_route(
    query: ComputeRouteQuery = Depends(),
    compute_route: IComputeRoute = Depends(),
) -> RouteResponse:
    return await compute_route.execute(command=ComputeRouteCommand(
            current_lat=query.current_lat,
            current_long=query.current_long,
            radius=query.radius
        )
    )