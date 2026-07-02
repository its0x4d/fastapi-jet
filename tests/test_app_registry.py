from fastapi_jet.app_registry import (
    resolve_app_template,
    suggest_installed_app_route,
    to_class_name,
)


def test_to_class_name():
    assert to_class_name("users") == "Users"
    assert to_class_name("user-profiles") == "UserProfiles"


def test_resolve_app_template():
    assert resolve_app_template(crud=False, versioned=False) == "app"
    assert resolve_app_template(crud=True, versioned=False) == "app-crud"
    assert resolve_app_template(crud=False, versioned=True) == "app-versioned"
    assert resolve_app_template(crud=True, versioned=True) == "app-crud-versioned"


def test_suggest_installed_app_route():
    assert (
        suggest_installed_app_route("users")
        == 'AppRoute(name="users", prefix="/users", tags=["users"]),'
    )
    assert (
        suggest_installed_app_route("users", versioned=True)
        == 'AppRoute(name="users", prefix="/v1/users", tags=["users"]),'
    )
