from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.routes.activities import router as activities_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Mergington High School API",
        description="API for viewing and signing up for extracurricular activities"
    )

    app.mount(
        "/static",
        StaticFiles(directory=str(Path(__file__).parent / "static")),
        name="static"
    )

    @app.get("/")
    def root():
        """Redirect root path to the static web application."""
        return RedirectResponse(url="/static/index.html")

    app.include_router(activities_router)
    return app


app = create_app()
