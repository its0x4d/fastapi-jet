import os

import typer
from questionary.form import form

from fastapi_jet.cli import app
from fastapi_jet.context import ProjectContext
from fastapi_jet.generator import generate_template
from fastapi_jet.utils import binary_question, name_fixer


@app.command(name="startproject")
def startproject(
        name: str = typer.Argument(
            ..., help="Name of the project",
            callback=lambda name: name_fixer(name),
            metavar="PROJECT_NAME"
        ),
        interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
        use_templates: bool = typer.Option(False, "--use-templates", "-t", help="Use templates"),
):
    """
    Start a new project
    """
    if interactive:
        project = form(
            use_templates=binary_question("Do you want to use templates?", default=True),
        ).ask()
    else:
        project = {
            "use_templates": use_templates,
        }

    typer.echo(f"[+] Creating project {name}...")
    generated = generate_template(
        template_name="project",
        context=ProjectContext(
            name=name,
            **project,
        )
    )

    if project["use_templates"]:
        typer.echo(f"[+] Creating templates in {generated}...")
        os.mkdir(os.path.join(generated, "templates"))
