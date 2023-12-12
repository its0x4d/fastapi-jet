import importlib
import os
from typing import Optional

import pkg_resources
import typer

try:
    import fastapi
except ImportError:
    raise ImportError("FastAPI is not installed. Please install it with: pip install fastapi")

app = typer.Typer(
    name="fastapi-jet",
    help="FastAPI-Jet - A tool to manage FastAPI projects",
    add_completion=False,
    invoke_without_command=False,
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    """
    Callback for the --version option.
    :return:
    """
    if value:
        package = pkg_resources.get_distribution("fastapi-jet")
        typer.echo(f"{package.project_name} {package.version}")
        raise typer.Exit()


def _register_commands() -> None:
    """
    Register all the commands.
    """
    for command in os.listdir(os.path.join(os.path.dirname(__file__), "commands")):
        if command.endswith(".py") and not command.startswith("__"):
            importlib.import_module(f"fastapi_jet.commands.{command[:-3]}")


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    ...


_register_commands()
