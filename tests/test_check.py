from pathlib import Path

from fastapi_jet.checks import all_checks_passed, run_project_checks


def _write_minimal_project(root: Path) -> None:
    (root / ".fastapi-jet").write_text('{"layout": "standard"}')
    (root / ".env").write_text("PROJECT_NAME=Demo\n")
    (root / "pyproject.toml").write_text(
        '[tool.fastapi-jet]\nlayout = "standard"\n'
    )
    base = root / "base"
    base.mkdir()
    apps = root / "apps" / "core"
    apps.mkdir(parents=True)
    (apps / "__init__.py").write_text("")
    (apps / "routers.py").write_text(
        "from fastapi import APIRouter\nrouter = APIRouter()\n"
    )
    (base / "routing.py").write_text(
        "import importlib\n"
        "from typing import TypedDict\n"
        "class AppRoute(TypedDict, total=False):\n"
        "    name: str\n"
        "    prefix: str\n"
        "def include_routers(fast_api_app, installed_apps, apps_path='apps'):\n"
        "    for app_route in installed_apps:\n"
        "        module = importlib.import_module(f'apps.{app_route[\"name\"]}.routers')\n"
        "        kwargs = {k: v for k, v in app_route.items() if k != 'name'}\n"
        "        fast_api_app.include_router(module.router, **kwargs)\n"
        "def include_middlewares(fast_api_app, middlewares):\n"
        "    pass\n"
    )
    (base / "core.py").write_text(
        "class Settings:\n    PROJECT_NAME = 'Demo'\nsettings = Settings()\n"
    )
    (base / "main.py").write_text(
        "from fastapi import FastAPI\n"
        "from base.core import settings\n"
        "from base.routing import AppRoute, include_middlewares, include_routers\n"
        "app = FastAPI(title=settings.PROJECT_NAME)\n"
        "@app.get('/health')\n"
        "async def health_check():\n"
        "    return {'status': 'ok'}\n"
        "INSTALLED_APPS = [{'name': 'core', 'prefix': '/core'}]\n"
        "include_middlewares(app, [])\n"
        "include_routers(app, INSTALLED_APPS)\n"
    )


def test_run_project_checks_passes_for_valid_layout(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)
    results = run_project_checks(tmp_path)
    assert all_checks_passed(results)


def test_run_project_checks_fails_when_main_missing(tmp_path: Path) -> None:
    _write_minimal_project(tmp_path)
    (tmp_path / "base" / "main.py").unlink()
    results = run_project_checks(tmp_path)
    assert not all_checks_passed(results)


def test_is_fastapi_project_detects_marker_file(tmp_path, monkeypatch) -> None:
    from fastapi_jet.utils import is_fastapi_project

    (tmp_path / ".fastapi-jet").write_text("{}")
    monkeypatch.chdir(tmp_path)
    assert is_fastapi_project() is True


def test_is_fastapi_project_detects_pyproject_marker(tmp_path, monkeypatch) -> None:
    from fastapi_jet.utils import is_fastapi_project

    base = tmp_path / "base"
    base.mkdir()
    (base / "main.py").write_text("# stub")
    (tmp_path / "pyproject.toml").write_text("[tool.fastapi-jet]\n")
    monkeypatch.chdir(tmp_path)
    assert is_fastapi_project() is True
