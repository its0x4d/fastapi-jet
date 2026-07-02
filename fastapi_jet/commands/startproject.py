
import typer
from questionary.form import form

from fastapi_jet.cli import app
from fastapi_jet.context import ProjectContext
from fastapi_jet.generator import generate_template
from fastapi_jet.utils import binary_question, name_fixer


@app.command(name="startproject")
def startproject(
    name: str = typer.Argument(
        ...,
        help="Project name",
        callback=lambda value: name_fixer(value),
        metavar="PROJECT_NAME",
    ),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactive mode"
    ),
    use_templates: bool = typer.Option(
        False, "--use-templates", "-t", help="Create a templates directory"
    ),
) -> None:
    """Create a new modular FastAPI project."""
    if interactive:
        project_options = form(
            use_templates=binary_question(
                "Do you want to use templates?", default=True
            ),
        ).ask()
    else:
        project_options = {"use_templates": use_templates}

    typer.echo(f"[+] Creating project {name}...")
    generated = generate_template(
        template_name="project",
        context=ProjectContext(name=name, **project_options),
    )

    if generated and project_options["use_templates"]:
        templates_dir = generated / "templates"
        templates_dir.mkdir(exist_ok=True)
        typer.echo(f"[+] Created templates directory at {templates_dir}")
