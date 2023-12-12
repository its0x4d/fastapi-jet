import typer

from fastapi_jet import utils
from fastapi_jet.cli import app
from fastapi_jet.context import AppContext
from fastapi_jet.decorators import fastapi_project
from fastapi_jet.generator import generate_template
from fastapi_jet.utils import name_fixer


@app.command(name="startapp")
@fastapi_project
def startapp(
        name: str = typer.Argument(..., help="Name of the project", callback=lambda name: name_fixer(name)),
):
    """
    Start a new FastAPI app
    """

    typer.echo(f"[+] Creating app {name}...")
    generate_template(
        template_name="app",
        context=AppContext(
            name=name
        )
    )
