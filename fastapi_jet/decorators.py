from functools import wraps

import typer

from fastapi_jet import utils


def fastapi_project(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if utils.is_fastapi_project():
            return f(*args, **kwargs)
        else:
            typer.echo("[!] This is not a fastapi-jet project. Please run this command from the project root.")
            raise typer.Exit()

    return decorated_function
