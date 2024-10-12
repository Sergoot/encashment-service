from fastapi import FastAPI

import aiohttp

def create_app():
    app = FastAPI()
    @app.get("/test")
    async def test():
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://encashment:9002/testing",
            ) as raw_result:
                result: dict = await raw_result.json()
        
        return result
    return app


def app_factory():
    return create_app()