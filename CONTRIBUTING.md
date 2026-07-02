# Contributing to FastAPI-Jet

Thank you for your interest in contributing. This project follows a **modular FastAPI / Django-inspired** workflow — keep changes focused and aligned with [docs/CONVENTIONS.md](docs/CONVENTIONS.md).

## Development setup

```bash
git clone https://github.com/its0x4d/fastapi-jet.git
cd fastapi-jet
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"  # or: pip install -e . pytest ruff pre-commit
pre-commit install
```

## Before opening a PR

```bash
ruff check .
pytest
```

CI must pass on Python 3.10–3.13.

## Project structure

```
fastapi_jet/
├── commands/       # Typer CLI commands
├── templates/      # Cookiecutter project & app templates
├── checks.py       # jet check validation
├── register.py     # AST-based INSTALLED_APPS registration
└── tools.py        # Routing helpers (keep in sync with template routing.py)
```

## Adding a CLI command

1. Create `fastapi_jet/commands/<name>.py`
2. Use `@app.command` — commands auto-register via `cli.py`
3. Project-only commands need `@fastapi_project`
4. Add tests in `tests/` using `typer.testing.CliRunner`

## Changing app templates

When editing routing/bootstrap logic, update **both**:

- `fastapi_jet/templates/project/.../base/routing.py`
- `fastapi_jet/tools.py`

Generated projects must **not** import `fastapi-jet` at runtime.

## Commit messages

Use clear, imperative subjects:

- `Add jet check command for project validation`
- `Fix include_routers apps_path mutation`

## Pull requests

- One concern per PR when possible
- Update `CHANGELOG.md` under `[Unreleased]` for user-facing changes
- Add tests for new behavior

## Reporting issues

Include:

- Python version
- `fastjet --version`
- Steps to reproduce
- Expected vs actual behavior

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
