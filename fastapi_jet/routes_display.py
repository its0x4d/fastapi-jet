import importlib
from typing import Any


def _route_tags(route: Any) -> str:
    tags = getattr(route, "tags", None) or []
    return ", ".join(tags)


def _dependency_count(route: Any) -> int:
    dependant = getattr(route, "dependant", None)
    if dependant is None:
        return 0
    return len(getattr(dependant, "dependencies", []) or [])


def _path_params(route: Any) -> str:
    dependant = getattr(route, "dependant", None)
    if dependant is None:
        return ""
    return ", ".join(param.name for param in dependant.path_params)


def collect_route_rows(
    installed_apps: list[dict[str, Any]],
    *,
    app_name: str = "all",
) -> list[list[str]]:
    rows: list[list[str]] = []
    for installed_app in installed_apps:
        if app_name != "all" and installed_app["name"] != app_name:
            continue
        router_module = importlib.import_module(
            f"apps.{installed_app['name']}.routers"
        )
        mount_prefix = installed_app.get("prefix", "")
        for route in router_module.router.routes:
            methods = getattr(route, "methods", None) or set()
            rows.append(
                [
                    installed_app["name"],
                    f"{mount_prefix}{route.path}",
                    ",".join(sorted(methods)),
                    route.name or "",
                    _route_tags(route),
                    str(_dependency_count(route)),
                    _path_params(route),
                ]
            )
    return rows
