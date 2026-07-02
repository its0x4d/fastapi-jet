import ast
from dataclasses import dataclass
from pathlib import Path

from fastapi_jet.app_registry import suggest_installed_app_route


class RegistrationError(Exception):
    """Raised when INSTALLED_APPS cannot be updated safely."""


@dataclass(frozen=True)
class RegistrationResult:
    registered: bool
    already_present: bool = False


def _find_installed_apps_list(tree: ast.Module) -> ast.List | None:
    for node in tree.body:
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "INSTALLED_APPS":
                if isinstance(node.value, ast.List):
                    return node.value
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "INSTALLED_APPS":
                    if isinstance(node.value, ast.List):
                        return node.value
    return None


def _app_route_name(node: ast.expr) -> str | None:
    if not isinstance(node, ast.Call):
        return None
    func = node.func
    if not (isinstance(func, ast.Name) and func.id == "AppRoute"):
        return None
    for keyword in node.keywords:
        if keyword.arg == "name" and isinstance(keyword.value, ast.Constant):
            if isinstance(keyword.value.value, str):
                return keyword.value.value
    return None


def _list_contains_app(app_list: ast.List, app_name: str) -> bool:
    for element in app_list.elts:
        if _app_route_name(element) == app_name:
            return True
    return False


def _indent_for_entry(lines: list[str], app_list: ast.List) -> str:
    if app_list.elts:
        last_line = lines[app_list.elts[-1].end_lineno - 1]
        return " " * (len(last_line) - len(last_line.lstrip()))
    open_line = lines[app_list.lineno - 1]
    base_indent = len(open_line) - len(open_line.lstrip())
    return " " * (base_indent + 4)


def _insertion_index(app_list: ast.List) -> int:
    if app_list.elts:
        return app_list.elts[-1].end_lineno
    return app_list.lineno


def register_app_in_main(
    main_path: Path,
    app_name: str,
    *,
    versioned: bool = False,
) -> RegistrationResult:
    source = main_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    app_list = _find_installed_apps_list(tree)
    if app_list is None:
        raise RegistrationError(
            "Could not find `INSTALLED_APPS = [...]` in base/main.py. "
            "Add the app manually."
        )

    if _list_contains_app(app_list, app_name):
        return RegistrationResult(registered=False, already_present=True)

    lines = source.splitlines(keepends=True)
    indent = _indent_for_entry(lines, app_list)
    entry = f"{indent}{suggest_installed_app_route(app_name, versioned=versioned)}\n"
    insert_at = _insertion_index(app_list)
    lines.insert(insert_at, entry)
    main_path.write_text("".join(lines), encoding="utf-8")
    return RegistrationResult(registered=True)
