import aiohttp
from bff.application.common.interfaces import ApiClient


class InternalApiClientAdapter(ApiClient):
    def __init__(
        self, 
        base_host: str,
        protocol: str = "http",
    ):
        self._base_uri = f"{protocol}://{base_host}"


    async def get(self, url: str, query_data: dict | None = None) -> dict:
        query_data = query_data or {}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self._base_uri}/{url}", params=query_data,
            ) as raw_result:
                
                result: dict = await raw_result.json()

                return result

    async def post(self, url: str, data: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._base_uri}/{url}", json=data,
            ) as raw_result:
                
                result: dict = await raw_result.json()

                return result