from bff.application.common.interfaces import ApiClient
from bff.application.services.compute_route import ComputeRoute
from bff.adapters.api_client import InternalApiClientAdapter

    
def api_client_factory(base_uri: str, port: int) -> InternalApiClientAdapter:
    return InternalApiClientAdapter(base_host=base_uri, port=port)


def compute_route_factory(
    atm_client: ApiClient,
    algo_client: ApiClient,
) -> ComputeRoute:
    return ComputeRoute(atm_client, algo_client)
        