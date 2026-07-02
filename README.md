<p align="center">
  <img src="https://i.ibb.co/z7TNsRL/DALL-E-2023-12-12-15-33-36-A-modern-and-sleek-logo-for-a-web-development-project-named-Fast-API-Jet.png" alt="FastAPI-Jet" width="300" />
</p>

<p align="center"><em>Django's structure. FastAPI's speed.</em></p>

[![Package version](https://img.shields.io/pypi/v/fastapi-jet?color=%2334D058&label=pypi%20package)](https://pypi.org/project/fastapi-jet)
[![Downloads](https://img.shields.io/pypi/dm/fastapi-jet)](https://pypi.org/project/fastapi-jet)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fastapi-jet)](https://pypi.org/project/fastapi-jet)
[![Telegram](https://img.shields.io/badge/Telegram-join%20chat-blue.svg)](https://t.me/fastapi_jet)

## What is FastAPI-Jet?

**FastAPI-Jet** helps you build and manage **modular, multi-app FastAPI projects** with a familiar, Django-inspired workflow.

It is **not** a full-stack generator. It is a **structure and CLI** tool for teams who want clear app boundaries and commands that stay useful after day one.

## Who is it for?

- Teams outgrowing a single `main.py`
- Developers coming from Django who want `startproject` / `startapp`
- Tech leads defining a consistent FastAPI layout

## Quick start

```bash
pip install fastapi-jet

# Create a project
fastjet startproject myapi
cd myapi

# Install and run (generated project is self-contained)
pip install -e ".[dev]"
fastjet runserver
```

Visit http://127.0.0.1:8000/docs — you'll see a `/health` endpoint and a sample `core` app at `/core/`.

## CLI commands

| Command | Description |
|---------|-------------|
| `fastjet startproject <name>` | Create a modular project skeleton |
| `fastjet startapp <name>` | Add a new app under `apps/` |
| `fastjet startapp <name> --crud` | App with schemas, services, dependencies |
| `fastjet startapp <name> --versioned` | `/v1/<name>` prefix pattern |
| `fastjet startapp <name> --register` | Auto-add to `INSTALLED_APPS` (AST-safe) |
| `fastjet runserver` | Run the dev server (Uvicorn) |
| `fastjet apps` | List registered apps |
| `fastjet routes` | Show the full route map (tags, deps) |
| `fastjet check` | Validate structure, imports, and settings |
| `fastjet shell` | REPL with `app` and `settings` loaded |

Aliases: `fastapi-jet` and `fastjet`.

## Project layout

```
myapi/
├── base/
│   ├── main.py       # FastAPI app + INSTALLED_APPS
│   ├── core.py       # Settings
│   └── routing.py    # Router registration (no runtime jet dependency)
├── apps/
│   └── core/         # Sample app included in new projects
├── tests/
├── pyproject.toml
└── .fastapi-jet      # Project marker
```

### Adding a feature

```bash
fastjet startapp users
fastjet startapp billing --crud --register
fastjet startapp api --versioned
```

With `--register`, the app is added to `INSTALLED_APPS` in `base/main.py` automatically (AST-safe). Without it, the CLI prints the line to paste manually.

Register manually in `base/main.py` if you prefer:

```python
INSTALLED_APPS: list[AppRoute] = [
    AppRoute(name="core", prefix="/core", tags=["core"]),
    AppRoute(name="users", prefix="/users", tags=["users"]),
]
```

Then inspect your API:

```bash
fastjet routes
```

## What FastAPI-Jet is not

- Not a "generate my entire SaaS" tool — try [fastapi-forge](https://github.com/nwyrwas/fastapi-forge) or [fastapi-spawn](https://github.com/Bishwajitgarai/fastapi-spawn)
- Not zero-opinion raw FastAPI — use FastAPI directly if you want no structure
- Not schema-first codegen — try [feathers](https://github.com/Abdul-Muizz1310/feathers)

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for app layer structure and workflow.

## Contributing

Contributions are welcome. Before opening a PR:

```bash
pip install -e .
pip install pytest ruff pre-commit
ruff check .
pytest
pre-commit run --all-files
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for project conventions.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgements

Inspired by Django's project/app model and the [manage-fastapi](https://github.com/ycd/manage-fastapi) project.
