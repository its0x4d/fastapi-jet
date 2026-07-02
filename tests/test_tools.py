from unittest.mock import MagicMock, patch

from fastapi import APIRouter, FastAPI
from typer.testing import CliRunner

from fastapi_jet.cli import app as cli_app
from fastapi_jet.tools import include_middlewares, include_routers
from fastapi_jet.utils import is_fastapi_project, name_fixer

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(cli_app, ["--version"])
    assert result.exit_code == 0
    assert "fastapi-jet" in result.stdout
    assert "1.1.5" in result.stdout


def test_cli_help():
    result = runner.invoke(cli_app, ["--help"])
    assert result.exit_code == 0
    assert "startproject" in result.stdout
    assert "startapp" in result.stdout


def test_name_fixer_replaces_invalid_characters():
    assert name_fixer("My Cool App") == "My_Cool_App"
    assert name_fixer("api-v1", extra=["-"]) == "api_v1"


def test_is_fastapi_project_false(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert is_fastapi_project() is False


def test_is_fastapi_project_true(tmp_path, monkeypatch):
    base_dir = tmp_path / "base"
    base_dir.mkdir()
    (base_dir / "main.py").write_text("# stub")
    monkeypatch.chdir(tmp_path)
    assert is_fastapi_project() is True


def test_startapp_requires_fastapi_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(cli_app, ["startapp", "users"])
    assert result.exit_code == 1
    assert "not a fastapi-jet project" in result.stdout


def test_include_routers_registers_routes():
    api = FastAPI()
    users_router = APIRouter()

    @users_router.get("/users")
    async def list_users():
        return []

    module = MagicMock()
    module.router = users_router

    with patch.dict("sys.modules", {"apps.users.routers": module}):
        include_routers(
            api,
            installed_apps=[{"name": "users", "prefix": "/users"}],
        )

    paths = [route.path for route in api.routes if hasattr(route, "path")]
    assert "/users/users" in paths


def test_include_middlewares_adds_middleware():
    api = FastAPI()
    include_middlewares(
        api,
        middlewares=[
            (
                "fastapi.middleware.cors.CORSMiddleware",
                {"allow_origins": ["*"], "allow_methods": ["*"]},
            )
        ],
    )
    assert len(api.user_middleware) == 1


@patch("fastapi_jet.generator.cookiecutter")
def test_generate_template_returns_none_on_existing_output(mock_cookiecutter, tmp_path, monkeypatch):
    from cookiecutter.exceptions import OutputDirExistsException

    from fastapi_jet.context import ProjectContext
    from fastapi_jet.generator import generate_template

    monkeypatch.chdir(tmp_path)
    mock_cookiecutter.side_effect = OutputDirExistsException("exists")

    result = generate_template(
        template_name="project",
        context=ProjectContext(name="demo"),
    )
    assert result is None
