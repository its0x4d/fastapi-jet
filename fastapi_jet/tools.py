from typing import List, Tuple

from fastapi import FastAPI

from fastapi_jet.context import AppRoute


def include_routers(fast_api_app: FastAPI, installed_apps: List[AppRoute], apps_path: str = "apps") -> None:
    """
    This function is used to include routers from the ROUTERS list in the main file.

    :param fast_api_app: The FastAPI application where the routers will be included.
    :type fast_api_app: FastAPI
    :param installed_apps: A list of AppRoute objects, where each object contains the name of an app
    :type installed_apps: list
    :param apps_path: The path to the apps' folder. Defaults to "apps".
    :type apps_path: str, optional
    :return: None
    """
    for route in installed_apps:
        route_module = f"{route['name']}.routers" if apps_path == '.' else f"{apps_path}.{route['name']}.routers"
        _route = __import__(route_module, fromlist=["router"])
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
    :type middlewares: list
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
