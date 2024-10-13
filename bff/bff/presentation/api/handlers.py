from fastapi import APIRouter, Depends

from bff.application.common.interfaces import IComputeRoute, RouteResponse


router = APIRouter()


@router.get("/{team_id}", response_model=RouteResponse)
async def get_computed_routes(
    team_id: int,
    compute_route: IComputeRoute = Depends(),
) -> RouteResponse:
    return await compute_route.execute(team_id)