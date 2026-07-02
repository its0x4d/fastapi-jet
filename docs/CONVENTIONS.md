# App conventions

This document describes how to structure feature apps in a FastAPI-Jet project.

## Directory layout

Each app lives under `apps/<name>/`:

```
apps/users/
├── __init__.py
├── routers.py       # HTTP layer — thin, delegates to services
├── schemas.py       # Pydantic request/response models
├── services.py      # Business logic (testable without HTTP)
└── dependencies.py  # FastAPI Depends() callables
```

Generate this layout with:

```bash
fastjet startapp users --crud
```

## Layer responsibilities

### routers.py

- Define `APIRouter` and route handlers only
- Parse/validate input via Pydantic schemas
- Call service methods; map exceptions to HTTP errors
- No database or business rules here

### schemas.py

- `Create`, `Update`, and `Read` models per resource
- Shared field types and validators
- No I/O or framework imports beyond Pydantic

### services.py

- Plain Python classes or functions
- Accept schemas / primitives; return schemas or domain objects
- Easy to unit test without `TestClient`

### dependencies.py

- Wire services into routes with `Depends()`
- Per-request state (db sessions, auth) belongs here later

## Registering an app

**Recommended (automatic):**

```bash
fastjet startapp users --register
fastjet startapp billing --crud --versioned --register
```

This uses AST parsing to append an `AppRoute(...)` entry to `INSTALLED_APPS` in `base/main.py`. It skips registration if the app is already present and fails safely if the file layout is unexpected.

**Manual:** omit `--register` and paste the printed line:

```python
INSTALLED_APPS: list[AppRoute] = [
    AppRoute(name="core", prefix="/core", tags=["core"]),
    AppRoute(name="users", prefix="/users", tags=["users"]),
]
```

For versioned APIs:

```bash
fastjet startapp billing --versioned --register
```

```python
AppRoute(name="billing", prefix="/v1/billing", tags=["billing"]),
```

## Day-2 workflow

```bash
fastjet startapp orders --crud --register   # scaffold + register
fastjet check
fastjet routes                     # inspect route map
fastjet runserver
pytest
```

## Versioning

- Use `--versioned` when the app exposes a versioned surface (`/v1/...`)
- Keep version in the **mount prefix** (`INSTALLED_APPS`), not hardcoded in every route
- Breaking changes → new app folder or new prefix (`/v2/...`), not silent edits

## What to avoid

- Importing `fastapi_jet` inside generated apps (runtime dependency on the CLI)
- Business logic in route handlers
- Cross-app imports (`apps.users` importing from `apps.orders` internals) — extract shared code to a dedicated package if needed
