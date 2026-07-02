# FastAPI-Jet documentation

**Django's structure. FastAPI's speed.**

FastAPI-Jet is a CLI for modular, multi-app FastAPI projects. It is not a full-stack generator — it helps you **organize and grow** APIs with a Django-inspired workflow.

## Install

```bash
pip install fastapi-jet
```

## Commands

| Command | Description |
|---------|-------------|
| `fastjet startproject <name>` | Create a project |
| `fastjet startapp <name> [--crud] [--versioned] [--register]` | Add an app |
| `fastjet runserver` | Dev server |
| `fastjet check` | Validate project |
| `fastjet routes` | Route map |
| `fastjet shell` | REPL with app loaded |

## Learn more

- [Repository README](https://github.com/its0x4d/fastapi-jet/blob/main/README.md)
- [App conventions](CONVENTIONS.md)
- [Contributing](https://github.com/its0x4d/fastapi-jet/blob/main/CONTRIBUTING.md)
- [Examples](https://github.com/its0x4d/fastapi-jet/blob/main/examples/README.md)

## Local docs

```bash
pip install mkdocs-material
mkdocs serve
```
