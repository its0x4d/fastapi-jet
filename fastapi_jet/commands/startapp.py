import typer

from fastapi_jet.app_registry import resolve_app_template, suggest_installed_app_route
from fastapi_jet.cli import app
from fastapi_jet.context import AppContext
from fastapi_jet.decorators import fastapi_project
from fastapi_jet.generator import generate_template
from fastapi_jet.project import get_project_root
from fastapi_jet.register import RegistrationError, register_app_in_main
from fastapi_jet.utils import name_fixer


@app.command(name="startapp")
@fastapi_project
def startapp(
    name: str = typer.Argument(
        ...,
        help="App name",
        callback=lambda value: name_fixer(value),
    ),
    crud: bool = typer.Option(
        False,
        "--crud",
        help="Generate router, schemas, services, and dependencies stubs",
    ),
    versioned: bool = typer.Option(
        False,
        "--versioned",
        help="Use a /v1 prefix pattern for the app router",
    ),
    register: bool = typer.Option(
        False,
        "--register/--no-register",
        help="Add the app to INSTALLED_APPS in base/main.py",
    ),
) -> None:
    """Create a new app under apps/."""
    context = AppContext(name=name, crud=crud, versioned=versioned)
    template_name = resolve_app_template(crud=crud, versioned=versioned)
    typer.echo(f"[+] Creating app {context.folder_name} ({template_name})...")
    generated = generate_template(template_name=template_name, context=context)
    if not generated:
        raise typer.Exit(code=1)

    route_line = suggest_installed_app_route(
        context.folder_name,
        versioned=versioned,
    )

    if register:
        main_path = get_project_root() / "base" / "main.py"
        try:
            result = register_app_in_main(
                main_path,
                context.folder_name,
                versioned=versioned,
            )
        except RegistrationError as exc:
            typer.echo(f"[!] {exc}")
            typer.echo(f"[+] Add manually: {route_line}")
            raise typer.Exit(code=1) from exc

        if result.already_present:
            typer.echo(
                f"[!] `{context.folder_name}` is already in INSTALLED_APPS — skipped."
            )
        else:
            typer.echo(f"[+] Registered in INSTALLED_APPS ({main_path})")
    else:
        typer.echo("\n[+] Register in INSTALLED_APPS (base/main.py):")
        typer.echo(route_line)
        typer.echo("[i] Tip: pass --register to add automatically.")
