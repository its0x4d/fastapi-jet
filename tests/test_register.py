from pathlib import Path

import pytest

from fastapi_jet.register import (
    RegistrationError,
    register_app_in_main,
)

MAIN_TEMPLATE = '''\
from fastapi import FastAPI

from .routing import AppRoute, include_middlewares, include_routers

app = FastAPI()

INSTALLED_APPS: list[AppRoute] = [
    AppRoute(name="core", prefix="/core", tags=["core"]),
]

include_middlewares(fast_api_app=app, middlewares=[])
include_routers(fast_api_app=app, installed_apps=INSTALLED_APPS)
'''


@pytest.fixture
def main_file(tmp_path: Path) -> Path:
    base = tmp_path / "base"
    base.mkdir()
    path = base / "main.py"
    path.write_text(MAIN_TEMPLATE, encoding="utf-8")
    return path


def test_register_app_in_main_appends_route(main_file: Path):
    result = register_app_in_main(main_file, "users")
    assert result.registered is True
    content = main_file.read_text(encoding="utf-8")
    assert 'AppRoute(name="users", prefix="/users", tags=["users"])' in content
    assert content.index("core") < content.index("users")


def test_register_app_in_main_versioned_prefix(main_file: Path):
    register_app_in_main(main_file, "billing", versioned=True)
    content = main_file.read_text(encoding="utf-8")
    assert 'prefix="/v1/billing"' in content


def test_register_app_in_main_skips_duplicate(main_file: Path):
    register_app_in_main(main_file, "users")
    result = register_app_in_main(main_file, "users")
    assert result.registered is False
    assert result.already_present is True
    content = main_file.read_text(encoding="utf-8")
    assert content.count('name="users"') == 1


def test_register_app_in_main_raises_when_list_missing(tmp_path: Path):
    path = tmp_path / "base" / "main.py"
    path.parent.mkdir(parents=True)
    path.write_text("INSTALLED_APPS = 'invalid'\n", encoding="utf-8")
    with pytest.raises(RegistrationError):
        register_app_in_main(path, "users")


def test_register_app_in_main_empty_list(tmp_path: Path):
    path = tmp_path / "base" / "main.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        "from routing import AppRoute\n\n"
        "INSTALLED_APPS: list[AppRoute] = []\n",
        encoding="utf-8",
    )
    register_app_in_main(path, "users")
    assert 'AppRoute(name="users"' in path.read_text(encoding="utf-8")
