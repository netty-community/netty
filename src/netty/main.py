
from fastapi import FastAPI

from netty.web.routers import views


def create_app() -> FastAPI:
    app = FastAPI(
        title="Netty Automation Tools",
        version="0.1.0",
        summary="Netty Automation Tools",
        description="Netty Automation Tools",
        docs_url="/api/docs",
    )

    @app.get(
        "/api/health", include_in_schema=False, tags=["Internal"]
    )
    def health() -> dict[str, str]:
        return {"status": "ok"}


    app.include_router(views)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
