import typer

from fastapi_jet.checks import run_project_checks
from fastapi_jet.cli import app
from fastapi_jet.decorators import fastapi_project
from fastapi_jet.project import get_project_root


@app.command(name="check")
@fastapi_project
def check_project() -> None:
    """Validate project structure, imports, and registered apps."""
    results = run_project_checks(get_project_root())
    failures = 0
    for result in results:
        prefix = "[+]" if result.passed else "[!]"
        line = f"{prefix} {result.name}"
        if not result.passed and result.detail:
            line = f"{line} — {result.detail}"
        typer.echo(line)
        if not result.passed:
            failures += 1

    if failures:
        typer.echo(f"\n[!] {failures} check(s) failed.")
        raise typer.Exit(code=1)

    typer.echo("\n[+] Project check passed.")
