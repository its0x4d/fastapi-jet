import tabulate
import typer

from fastapi_jet.cli import app
from fastapi_jet.decorators import fastapi_project
from fastapi_jet.project import load_main_module
from fastapi_jet.routes_display import collect_route_rows


@app.command(name="apps")
@fastapi_project
def app_list() -> None:
    """List installed apps."""
    main_module = load_main_module()
    apps_table = [
        [
            route["name"],
            route.get("prefix", ""),
            f"apps/{route['name']}/routers.py",
        ]
        for route in main_module.INSTALLED_APPS
    ]
    typer.echo(
        tabulate.tabulate(
            apps_table,
            headers=["App Name", "Prefix", "Router Path"],
            tablefmt="rounded_outline",
        )
    )
    typer.echo(
        "[!] Missing an app? Register it in INSTALLED_APPS in base/main.py"
    )


@app.command(name="routes")
@fastapi_project
def routes_list(
    app_name: str = typer.Option(
        "all", "--app", "-a", help="App name to filter routes"
    ),
) -> None:
    """List routes for all apps or one app."""
    main_module = load_main_module()
    rows = collect_route_rows(main_module.INSTALLED_APPS, app_name=app_name)
    typer.echo(
        tabulate.tabulate(
            rows,
            headers=[
                "App",
                "Path",
                "Methods",
                "Name",
                "Tags",
                "Deps",
                "Parameters",
            ],
            tablefmt="rounded_outline",
        )
    )
