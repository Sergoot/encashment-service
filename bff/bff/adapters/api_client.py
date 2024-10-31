import logging

import aiohttp
from bff.application.common.interfaces import ApiClient



class InternalApiClientAdapter(ApiClient):
    def __init__(
        self, 
        base_host: str,
        port: int,
        protocol: str = "http",
    ):
        self._base_uri = f"{protocol}://{base_host}:{port}"

    async def get(self, url: str, query_data: dict | None = None) -> dict | list:
        query_data = query_data or {}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self._base_uri}/{url}", params=query_data,
            ) as raw_result:
                raw_result.raise_for_status()
                result = await raw_result.json()
                
                return result

    async def post(self, url: str, data: dict | list) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._base_uri}/{url}", json=data,
            ) as raw_result:
                raw_result.raise_for_status()
                result: dict = await raw_result.json()

                return result