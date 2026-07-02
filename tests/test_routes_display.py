from fastapi import APIRouter

from fastapi_jet.routes_display import collect_route_rows


def test_collect_route_rows_includes_tags_and_prefix():
    router = APIRouter()

    @router.get("/items", tags=["items"])
    async def list_items():
        return []

    module_name = "apps.testapp.routers"
    import sys
    from types import ModuleType

    module = ModuleType(module_name)
    module.router = router
    sys.modules[module_name] = module

    rows = collect_route_rows(
        [{"name": "testapp", "prefix": "/testapp"}],
        app_name="all",
    )
    assert rows[0][1] == "/testapp/items"
    assert rows[0][4] == "items"
    assert rows[0][5] == "0"

    del sys.modules[module_name]
