from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def _noop_cookiecutter_replay_dump():
    with patch("cookiecutter.replay.dump", return_value=None):
        yield


@pytest.fixture
def cookiecutter_env(tmp_path, monkeypatch):
    """Isolate cookiecutter replay/config writes to a temp home directory."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    (tmp_path / ".cookiecutter_replay").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    return tmp_path
