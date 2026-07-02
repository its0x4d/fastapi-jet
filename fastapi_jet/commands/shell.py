import code
import importlib

from fastapi_jet.cli import app
from fastapi_jet.decorators import fastapi_project
from fastapi_jet.project import ensure_project_on_path, load_main_module


@app.command(name="shell")
@fastapi_project
def project_shell() -> None:
    """Open a Python shell with the FastAPI app and settings loaded."""
    ensure_project_on_path()
    main_module = load_main_module()
    settings = importlib.import_module("base.core").settings
    banner = (
        "FastAPI-Jet shell — `app` is the FastAPI instance, "
        "`settings` is loaded from base.core"
    )
    code.interact(
        banner=banner,
        local={
            "app": main_module.app,
            "settings": settings,
            "INSTALLED_APPS": main_module.INSTALLED_APPS,
        },
    )
