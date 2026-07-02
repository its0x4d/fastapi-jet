# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-07-02

### Added
- `startapp --register` — AST-safe auto-registration in `INSTALLED_APPS`
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, GitHub issue/PR templates
- `examples/README.md` with end-to-end workflows
- MkDocs config (`mkdocs.yml`, `docs/index.md`)
- PyPI release workflow (tag `v*` → publish)
- CI matrix: Python 3.13
- `startapp --crud` — router, schemas, services, and dependencies stubs
- `startapp --versioned` — `/v1/<app>` prefix registration pattern
- `startapp` prints the exact `INSTALLED_APPS` line to add after scaffolding
- `jet shell` — REPL with `app` and `settings` in local scope
- Richer `jet routes` output (tags, dependency count, mounted path)
- `jet apps` shows mount prefix per app
- `docs/CONVENTIONS.md` — app layer structure and day-2 workflow
- `jet check` command — validates structure, imports, settings, and `/health`
- Generated project template: `pyproject.toml`, `.env.example`, `.fastapi-jet` marker
- Sample `core` app pre-registered in `INSTALLED_APPS`
- `/health` endpoint on new projects
- Pytest scaffold with smoke tests in generated projects
- `__init__.py` files for apps and app template

### Changed
- README rewritten around Option A positioning (modular FastAPI workflow)
- Generated project README is project-specific with layout and commands
- `is_fastapi_project()` recognizes `.fastapi-jet` and `pyproject.toml` markers
- Ruff linting and pre-commit hooks
- CLI integration tests
- `CHANGELOG.md`
- Shared `fastapi_jet.project` module for runtime cwd/path handling
- Cleaner CLI startup (removed redundant FastAPI import guard)
- `name_fixer` uses `str.translate` for single-pass sanitization
- `importlib.import_module` replaces `__import__` across routing utilities
- Added `.cursor/rules/fastapi-jet.mdc` contributor standards for AI and humans
- Minimum supported Python raised to 3.10 (CI matrix: 3.10–3.13)

### Fixed
- `runserver` no longer passes project directory as Uvicorn `root_path`
- Corrected app path references (`routers.py`, `INSTALLED_APPS` in `base/main.py`)
- `routes` command now requires a fastapi-jet project
- `@fastapi_project` now exits with code 1 when outside a project
- `include_routers` no longer mutates `apps_path` inside the loop
- Generator no longer returns a success path when output already exists
- CI on Python 3.13 (refreshed `poetry.lock` with Pydantic builds that ship cp313 wheels)
