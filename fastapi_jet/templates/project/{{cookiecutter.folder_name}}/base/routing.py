import importlib
from typing import Any, TypedDict

from fastapi import FastAPI


class AppRoute(TypedDict, total=False):
    name: str
    prefix: str
    tags: list[str]


def _router_module_path(app_name: str, apps_path: str) -> str:
    apps_module = apps_path.replace("/", ".")
    if apps_module == ".":
        return f"{app_name}.routers"
    return f"{apps_module}.{app_name}.routers"


def include_routers(
    fast_api_app: FastAPI,
    installed_apps: list[AppRoute],
    apps_path: str = "apps",
) -> None:
    for app_route in installed_apps:
        module = importlib.import_module(
            _router_module_path(app_route["name"], apps_path)
        )
        router_kwargs = {
            key: value for key, value in app_route.items() if key != "name"
        }
        fast_api_app.include_router(module.router, **router_kwargs)


def include_middlewares(
    fast_api_app: FastAPI,
    middlewares: list[tuple[str, dict[str, Any]]],
) -> None:
    for middleware_path, middleware_config in middlewares:
        module_path, _, class_name = middleware_path.rpartition(".")
        module = importlib.import_module(module_path)
        middleware = getattr(module, class_name)
        fast_api_app.add_middleware(middleware, **middleware_config)
