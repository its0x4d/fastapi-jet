import os
import sys
import typer
import uvicorn

from fastapi_jet.cli import app
from fastapi_jet.constants import PROJECT_ROOT
from fastapi_jet.decorators import fastapi_project

sys.path.append(PROJECT_ROOT)


@app.command(name="runserver")
@fastapi_project
def run_server(
        host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host of the server"),
        port: int = typer.Option(8000, "--port", "-p", help="Port of the server"),
        no_reload: bool = typer.Option(False, "--no-reload", "-nr", help="Disable auto-reload when code changes"),
        log_level: str = typer.Option("info", "--log-level", "-ll", help="Log level"),
):
    """
    Run the server.

    Default app directory is `app.main:app` and can be changed with FASTAPI_APP environment variable.
    """
    app_path = os.environ.get("FASTAPI_APP", "base.main:app")
    uvicorn.run(
        app_path,
        host=host,
        port=port,
        reload=not no_reload,
        root_path=PROJECT_ROOT,
        log_level=log_level,
    )
