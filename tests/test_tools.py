from fastapi import FastAPI
from fastapi_jet.tools import include_routers
from fastapi_jet.context import AppRoute


def test_app():
    app = FastAPI(title="FastAPI Jet")
    assert app.title == "FastAPI Jet"