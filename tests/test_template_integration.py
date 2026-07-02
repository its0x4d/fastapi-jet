import sys

import pytest
from typer.testing import CliRunner

from fastapi_jet.cli import app as cli_app

runner = CliRunner()


@pytest.fixture
def clean_modules():
    preserved = {
        key: value
        for key, value in sys.modules.items()
        if not key.startswith(("base", "apps"))
    }
    yield
    for key in list(sys.modules):
        if key.startswith(("base", "apps")) and key not in preserved:
            del sys.modules[key]


def test_startproject_generates_runnable_layout(
    tmp_path, monkeypatch, clean_modules, cookiecutter_env
):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(cli_app, ["startproject", "demo"])
    assert result.exit_code == 0, result.stdout

    project_dir = tmp_path / "demo"
    assert project_dir.is_dir()
    assert (project_dir / "pyproject.toml").is_file()
    assert (project_dir / "apps" / "core" / "routers.py").is_file()
    assert (project_dir / "tests" / "test_app.py").is_file()

    monkeypatch.chdir(project_dir)
    check_result = runner.invoke(cli_app, ["check"])
    assert check_result.exit_code == 0, check_result.stdout
    assert "Project check passed" in check_result.stdout


def test_cli_lists_check_command():
    result = runner.invoke(cli_app, ["--help"])
    assert result.exit_code == 0
    assert "check" in result.stdout
    assert "shell" in result.stdout


def test_startapp_crud_generates_service_layer(
    tmp_path, monkeypatch, clean_modules, cookiecutter_env
):
    monkeypatch.chdir(tmp_path)

    project_result = runner.invoke(cli_app, ["startproject", "demo"])
    assert project_result.exit_code == 0, project_result.stdout

    project_dir = tmp_path / "demo"
    monkeypatch.chdir(project_dir)

    app_result = runner.invoke(cli_app, ["startapp", "items", "--crud"])
    assert app_result.exit_code == 0, app_result.stdout
    assert "AppRoute" in app_result.stdout

    app_dir = project_dir / "apps" / "items"
    assert (app_dir / "schemas.py").is_file()
    assert (app_dir / "services.py").is_file()
    assert (app_dir / "dependencies.py").is_file()
    assert (app_dir / "routers.py").is_file()
    assert "ItemsService" in (app_dir / "services.py").read_text(encoding="utf-8")


def test_startapp_register_updates_installed_apps(
    tmp_path, monkeypatch, clean_modules, cookiecutter_env
):
    monkeypatch.chdir(tmp_path)
    runner.invoke(cli_app, ["startproject", "demo"])
    project_dir = tmp_path / "demo"
    monkeypatch.chdir(project_dir)

    result = runner.invoke(cli_app, ["startapp", "billing", "--register"])
    assert result.exit_code == 0, result.stdout
    assert "Registered in INSTALLED_APPS" in result.stdout

    main_content = (project_dir / "base" / "main.py").read_text(encoding="utf-8")
    assert 'AppRoute(name="billing", prefix="/billing"' in main_content

