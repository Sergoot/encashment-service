from bff.application.common.interfaces import ApiClient, IComputeRoute, RouteResponse
from bff.application.common.commands import ComputeRouteCommand


class ComputeRoute(IComputeRoute):
    def __init__(
        self,
        atm_api_client: ApiClient,
        algo_api_client: ApiClient,
    ) -> None:
        self.atm_client = atm_api_client
        self.algo_client = algo_api_client
        
    def _build_query(self, command: ComputeRouteCommand) -> dict:
        return {
            "lat": command.current_lat,
            "long": command.current_long,
            "radius": command.radius,
        }
    
    async def execute(self, command: ComputeRouteCommand) -> RouteResponse:
        attempts_to_get_atms = 3
        atm_response = await self.atm_client.get(
            "api/v1/atm/closest", 
            query_data=self._build_query(command)
        )
        if not atm_response:
            for _ in range(attempts_to_get_atms):
                command.radius = int(command.radius*1.5)
                if fallback_response := await self.atm_client.get(
                    "api/v1/atm/closest", 
                    query_data=self._build_query(command)
                ):
                    atm_response = fallback_response
                    break
            else:
                return RouteResponse(next_step="FINAL")

        algo_request = {
            "current_lat": command.current_lat,
            "current_long": command.current_long,
            "atms": atm_response 
        }
            
        next_step_response = await self.algo_client.post("compute/next", data=algo_request)
        await self.atm_client.patch(
            f"api/v1/atm/{next_step_response['id']}",
            data={"money_current": next_step_response['capacity']['max']}
        )
        return RouteResponse(next_step=next_step_response)
