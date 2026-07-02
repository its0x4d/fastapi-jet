from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

import typer

from fastapi_jet.utils import is_fastapi_project

P = ParamSpec("P")
R = TypeVar("R")


def fastapi_project(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not is_fastapi_project():
            typer.echo(
                "[!] This is not a fastapi-jet project. "
                "Run this command from the project root."
            )
            raise typer.Exit(code=1)
        return func(*args, **kwargs)

    return wrapper
