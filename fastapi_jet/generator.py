from pathlib import Path
from typing import Union

import typer
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter

from fastapi_jet.constants import TEMPLATES_DIR
from fastapi_jet.context import AppContext, ProjectContext


def _is_app_template(template_name: str) -> bool:
    return template_name == "app" or template_name.startswith("app-")


def _output_path(template_name: str, folder_name: str, cwd: Path) -> Path:
    if _is_app_template(template_name):
        return cwd / "apps" / folder_name
    return cwd / folder_name


def generate_template(
    template_name: str, context: Union[ProjectContext, AppContext]
) -> Path | None:
    cwd = Path.cwd()
    output_path = _output_path(template_name, context.folder_name, cwd)

    cookiecutter_kwargs = {
        "template": str(TEMPLATES_DIR / template_name),
        "no_input": True,
        "extra_context": context.model_dump(),
        "overwrite_if_exists": False,
    }
    if _is_app_template(template_name):
        cookiecutter_kwargs["output_dir"] = str(cwd / "apps")

    try:
        cookiecutter(**cookiecutter_kwargs)
    except OutputDirExistsException:
        typer.echo(
            "[!] Unable to create FastAPI app! "
            "An item with the same name already exists.\n"
            "[+] Choose a different name or delete the existing one and try again."
        )
        return None

    typer.echo(f"[+] App [{context.folder_name}] created successfully!")
    return output_path
