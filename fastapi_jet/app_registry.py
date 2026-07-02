def to_class_name(folder_name: str) -> str:
    """Convert an app folder name into a PascalCase class prefix."""
    return "".join(
        part.capitalize() for part in folder_name.replace("-", "_").split("_") if part
    )


def resolve_app_template(*, crud: bool, versioned: bool) -> str:
    if crud and versioned:
        return "app-crud-versioned"
    if crud:
        return "app-crud"
    if versioned:
        return "app-versioned"
    return "app"


def suggest_installed_app_route(name: str, *, versioned: bool = False) -> str:
    prefix = f"/v1/{name}" if versioned else f"/{name}"
    return f'AppRoute(name="{name}", prefix="{prefix}", tags=["{name}"]),'
