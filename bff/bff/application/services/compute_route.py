from bff.application.common.interfaces import ApiClient, IComputeRoute, RouteResponse


class ComputeRoute(IComputeRoute):
    def __init__(
        self,
        atm_api_client: ApiClient,
        algo_api_client: ApiClient,
    ) -> None:
        self.atm_client = atm_api_client
        self.algo_client = algo_api_client
        
    
    async def execute(self, encash_team_id: int) -> RouteResponse:
        atm_response = await self.atm_client.get("api/v1/atm")
        # TODO some logic with atm_reponse
        raw_routes_response = await self.algo_client.post("compute", data=atm_response)
        return RouteResponse(routes=raw_routes_response["routes"])
