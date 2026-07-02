import os

import typer
import uvicorn

from fastapi_jet.cli import app
from fastapi_jet.decorators import fastapi_project
from fastapi_jet.project import ensure_project_on_path


@app.command(name="runserver")
@fastapi_project
def run_server(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host"),
    port: int = typer.Option(8000, "--port", "-p", help="Port"),
    no_reload: bool = typer.Option(
        False, "--no-reload", "-nr", help="Disable auto-reload"
    ),
    log_level: str = typer.Option("info", "--log-level", "-ll", help="Log level"),
    root_path: str = typer.Option(
        "",
        "--root-path",
        help="URL prefix when running behind a reverse proxy",
    ),
) -> None:
    """Run the development server."""
    project_root = ensure_project_on_path()
    app_path = os.environ.get("FASTAPI_APP", "base.main:app")
    uvicorn_kwargs: dict = {
        "host": host,
        "port": port,
        "reload": not no_reload,
        "log_level": log_level,
    }
    if root_path:
        uvicorn_kwargs["root_path"] = root_path
    if not no_reload:
        uvicorn_kwargs["reload_dirs"] = [str(project_root)]
    uvicorn.run(app_path, **uvicorn_kwargs)
