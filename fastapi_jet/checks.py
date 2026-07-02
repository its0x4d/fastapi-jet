import importlib
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


REQUIRED_PATHS = (
    "base/main.py",
    "base/core.py",
    "base/routing.py",
    "apps",
    "pyproject.toml",
    ".env",
    ".fastapi-jet",
)


def _ensure_root_on_path(root: Path) -> None:
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def check_structure(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    for relative_path in REQUIRED_PATHS:
        target = root / relative_path
        if relative_path == "apps":
            exists = target.is_dir()
        else:
            exists = target.is_file()
        results.append(
            CheckResult(
                name=f"exists: {relative_path}",
                passed=exists,
                detail="" if exists else "missing",
            )
        )

    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        has_marker = "[tool.fastapi-jet]" in pyproject.read_text(encoding="utf-8")
        results.append(
            CheckResult(
                name="pyproject: [tool.fastapi-jet] marker",
                passed=has_marker,
                detail="" if has_marker else "marker not found",
            )
        )
    return results


def check_imports(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    _ensure_root_on_path(root)

    for module_name in ("base.main", "base.core"):
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            results.append(
                CheckResult(
                    name=f"import {module_name}",
                    passed=False,
                    detail=str(exc),
                )
            )
            return results
        results.append(CheckResult(name=f"import {module_name}", passed=True))

    try:
        core = importlib.import_module("base.core")
        project_name = core.settings.PROJECT_NAME
        if not project_name:
            raise ValueError("PROJECT_NAME is empty")
        results.append(CheckResult(name="settings: PROJECT_NAME", passed=True))
    except Exception as exc:
        results.append(
            CheckResult(
                name="settings: PROJECT_NAME",
                passed=False,
                detail=str(exc),
            )
        )
        return results

    main = importlib.import_module("base.main")
    installed_apps = getattr(main, "INSTALLED_APPS", None)
    if installed_apps is None:
        results.append(
            CheckResult(
                name="INSTALLED_APPS defined",
                passed=False,
                detail="INSTALLED_APPS missing on base.main",
            )
        )
        return results

    results.append(CheckResult(name="INSTALLED_APPS defined", passed=True))

    for app_route in installed_apps:
        app_name = app_route["name"]
        app_dir = root / "apps" / app_name
        router_file = app_dir / "routers.py"
        results.append(
            CheckResult(
                name=f"exists: apps/{app_name}/routers.py",
                passed=router_file.is_file(),
                detail="" if router_file.is_file() else "missing",
            )
        )
        module_name = f"apps.{app_name}.routers"
        try:
            importlib.import_module(module_name)
            results.append(
                CheckResult(name=f"import {module_name}", passed=True)
            )
        except Exception as exc:
            results.append(
                CheckResult(
                    name=f"import {module_name}",
                    passed=False,
                    detail=str(exc),
                )
            )

    health_route = any(
        getattr(route, "path", None) == "/health"
        for route in main.app.routes
    )
    results.append(
        CheckResult(
            name="route: /health",
            passed=health_route,
            detail="" if health_route else "not registered",
        )
    )
    return results


def run_project_checks(root: Path | None = None) -> list[CheckResult]:
    project_root = root or Path.cwd()
    return check_structure(project_root) + check_imports(project_root)


def all_checks_passed(results: list[CheckResult]) -> bool:
    return all(result.passed for result in results)
