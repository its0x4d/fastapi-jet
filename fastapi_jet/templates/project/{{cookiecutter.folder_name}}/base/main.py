from fastapi import FastAPI

from .core import settings
from .routing import AppRoute, include_middlewares, include_routers

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


INSTALLED_APPS: list[AppRoute] = [
    AppRoute(name="core", prefix="/core", tags=["core"]),
]

MIDDLEWARES = [
    (
        "fastapi.middleware.cors.CORSMiddleware",
        {
            "allow_origins": settings.BACKEND_CORS_ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
    )
]

include_middlewares(fast_api_app=app, middlewares=MIDDLEWARES)
include_routers(fast_api_app=app, installed_apps=INSTALLED_APPS)
