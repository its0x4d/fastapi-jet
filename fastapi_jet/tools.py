from typing import List, Tuple

from fastapi import FastAPI

from fastapi_jet.context import AppRoute


def include_routers(fast_api_app: FastAPI, installed_apps: List[AppRoute]) -> None:
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
    for route in installed_apps:
        _route = __import__(f"apps.{route['name']}.routers", fromlist=["router"])
        route = route.copy()
        route.pop('name')
        fast_api_app.include_router(_route.router, **route)


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
