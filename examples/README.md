# Examples

FastAPI-Jet projects are generated locally — this folder documents end-to-end workflows rather than shipping a full duplicate repo.

## Quick demo (5 minutes)

```bash
pip install fastapi-jet

# 1. Create project
fastjet startproject demo
cd demo
pip install -e ".[dev]"

# 2. Validate
fastjet check

# 3. Run
fastjet runserver
# → http://127.0.0.1:8000/health
# → http://127.0.0.1:8000/docs

# 4. Add a CRUD app (auto-register)
fastjet startapp products --crud --register

# 5. Inspect
fastjet apps
fastjet routes
fastjet check
pytest
```

## Versioned API app

```bash
fastjet startapp billing --versioned --register
fastjet routes --app billing
```

Routes mount at `/v1/billing/...` when registered with the suggested prefix.

## Day-2 workflow

| Step | Command |
|------|---------|
| Scaffold app | `fastjet startapp orders --crud --register` |
| Validate | `fastjet check` |
| Debug routes | `fastjet routes` |
| REPL | `fastjet shell` |
| Tests | `pytest` |

See [docs/CONVENTIONS.md](../docs/CONVENTIONS.md) for app layer structure.

## Sample generated layout

```
demo/
├── base/main.py          # INSTALLED_APPS + /health
├── apps/core/            # included in new projects
├── apps/products/        # after startapp --crud --register
│   ├── routers.py
│   ├── schemas.py
│   ├── services.py
│   └── dependencies.py
└── tests/test_app.py
```
