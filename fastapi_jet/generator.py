import os
from typing import Union

import typer
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter

from fastapi_jet.constants import TEMPLATES_DIR
from fastapi_jet.context import ProjectContext, AppContext


def generate_template(template_name: str, context: Union[ProjectContext, AppContext]) -> str:
    """
    This function is used to generate a template using the cookiecutter library.

    :param template_name: The name of the template to generate.
    :type template_name: str
    :param context: An object that contains the context for the template.
        This can be either a ProjectContext or an AppContext.
    :type context: Union[ProjectContext, AppContext]
    :return: The path to the generated template.
    :rtype: str
    """
    try:
        # Generate the template using the cookiecutter library. in 'apps' folder
        data = {
            'template': os.path.join(TEMPLATES_DIR, template_name),
            'no_input': True,
            'extra_context': context.dict(),
        }
        if template_name == "app":
            data['output_dir'] = os.path.join(os.getcwd(), 'apps')
        cookiecutter(**data)

    except OutputDirExistsException:
        typer.echo(
            f"[!] Unable to create FastAPI {template_name}! An app with the same name already exists!"
            f"\n[+] Please choose a different name or delete the existing app and try again."
        )
    else:
        text = (
            f"[+] {template_name.capitalize()} [{context.folder_name}] created successfully!"
        )
        if template_name == "app":
            text += f"\n[+] To get started, add your app to ROUTERS in app/main.py"
        typer.echo(text)

    return os.path.join(os.getcwd(), context.folder_name)
