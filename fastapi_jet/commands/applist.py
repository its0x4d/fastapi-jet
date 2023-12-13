import sys

import tabulate
import typer

from fastapi_jet.cli import app
from fastapi_jet.constants import PROJECT_ROOT
from fastapi_jet.decorators import fastapi_project

sys.path.append(PROJECT_ROOT)


@app.command(name="apps")
@fastapi_project
def app_list():
    """
    Show all apps
    """

    main_core = __import__("base.main", fromlist=["main"])
    apps_table = []
    for route in main_core.ROUTERS:
        apps_table += [
            [route['name'], f"apps/{route['name']}/router.py"],
        ]
    table = tabulate.tabulate(apps_table, headers=["App Name", "AppRoute Path"], tablefmt="rounded_outline")
    print(table)
    print('[!] If you cant see your app in the list, make sure you have added it to ROUTERS in app/main.py')


@app.command(name="routes")
def routes_list(
        app_name: str = typer.Option("all", "--app", "-a", help="Name of the app to list routes for"),
):
    """
    Show routes for all apps or a specific app
    """

    main_core = __import__("base.main", fromlist=["main"])
    main_routes = []
    for _route in main_core.ROUTERS:
        if app_name != "all" and _route['name'] != app_name:
            continue
        imported_app = __import__(f"apps.{_route['name']}.routers", fromlist=["router"])
        routes_table = []
        for route in imported_app.router.routes:
            routes_table.append([
                _route['name'],
                route.path,
                ",".join(route.methods),
                route.name,
                ", ".join([
                    x.name for x in route.dependant.path_params
                ])
            ])
        main_routes += routes_table

    table = tabulate.tabulate(
        main_routes,
        headers=[
            "App Name",
            "Path",
            "Methods",
            "Name",
            "Parameters"
        ],
        tablefmt="rounded_outline",

    )
    print(table)
