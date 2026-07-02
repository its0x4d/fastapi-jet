import importlib
from importlib.metadata import PackageNotFoundError, version

import typer

from fastapi_jet.constants import COMMANDS_DIR

app = typer.Typer(
    name="fastapi-jet",
    help="FastAPI-Jet - modular FastAPI project management",
    add_completion=False,
    invoke_without_command=False,
    no_args_is_help=True,
)


def _get_version() -> str:
    try:
        return version("fastapi-jet")
    except PackageNotFoundError:
        from fastapi_jet import __version__

        return __version__


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"fastapi-jet {_get_version()}")
        raise typer.Exit()


def _register_commands() -> None:
    for command_file in COMMANDS_DIR.iterdir():
        if command_file.suffix == ".py" and not command_file.name.startswith("__"):
            importlib.import_module(f"fastapi_jet.commands.{command_file.stem}")


@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """Manage modular FastAPI projects with a Django-inspired workflow."""


_register_commands()
