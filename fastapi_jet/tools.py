from typing import List, Tuple

import typer
from fastapi import FastAPI


def include_routers(fast_api_app: FastAPI, installed_apps: list) -> None:
    """
    This function is used to include routers from installed apps into the FastAPI application.

    :param fast_api_app: The FastAPI application where the routers will be included.
    :type fast_api_app: FastAPI
    :param installed_apps: A list of tuples, where each tuple contains the name of an
        installed app and its corresponding prefix.
    :type installed_apps: list
    :return: None
    """
    # Loop over the installed apps.
    for app_name, prefix in installed_apps:
        try:
            # Try to import the router from the app.
            _app = __import__(f"{app_name}.router", fromlist=["router"])
        except ImportError:
            # If the import fails, print an error message and raise the exception.
            typer.echo(
                f"[!] Unable to import {app_name}.router. Please make sure it exists and try again."
            )
            raise
        # Check if the FastAPI application has a 'router' attribute.
        if not hasattr(fast_api_app, "router"):
            # If not, raise an AttributeError with a helpful error message.
            raise AttributeError(
                f"Router not found in {app_name}.router. Please add `router` attribute in {app_name}/router.py"
            )
        # Include the router from the app into the FastAPI application.
        fast_api_app.include_router(_app.router, prefix=prefix)


def include_middlewares(fast_api_app: FastAPI, middlewares: List[Tuple[str, dict]]) -> None:
    """
    This function is used to include middlewares into the FastAPI application.

    :param fast_api_app: The FastAPI application where the middlewares will be included.
    :type fast_api_app: FastAPI
    :param middlewares: A list of tuples, where each tuple contains the name of a middleware
        and its corresponding configuration.
    :type middlewares: List[Tuple[str, dict]]
    :return: None
    """
    # Loop over the middlewares.
    for middleware_name, middleware_config in middlewares:
        _middleware_class = middleware_name.split(".")[-1]
        _middleware_module = middleware_name.replace(f".{_middleware_class}", "")
        _middleware = __import__(
            _middleware_module, fromlist=[_middleware_class]
        ).__dict__[_middleware_class]

        # Add the middleware to the FastAPI application.
        fast_api_app.add_middleware(_middleware, **middleware_config)
