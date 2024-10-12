from fastapi import FastAPI


def create_app():
    app = FastAPI()
    @app.get("/testing")
    def testing():
        return {"status": 200}
    return app


def app_factory():
    return create_app()
