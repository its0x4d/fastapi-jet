from fastapi import FastAPI

from fastapi_jet.tools import include_routers, include_middlewares
from .core import settings

# Create a FastAPI application with the project name as the title.
app = FastAPI(title=settings.PROJECT_NAME)

# The first element is the app name and the second element is the app's prefix.
# To enable app routers, add them here along with their prefixes.
# e.g. ("auth_app", "/v1/auth", ADD_TAGS_HERE)
INSTALLED_APPS = [
]


# The first element is the middleware class and the second element is a dictionary of options for the middleware.
MIDDLEWARES = [
    ('fastapi.middleware.cors.CORSMiddleware', {
        'allow_origins': settings.BACKEND_CORS_ORIGINS,
        'allow_credentials': True,
        'allow_methods': ["*"],
        'allow_headers': ["*"],
    })
]


# Include the middlewares in the FastAPI application.
include_middlewares(fast_api_app=app, middlewares=MIDDLEWARES)
# Include the routers from the installed apps in the FastAPI application.
include_routers(fast_api_app=app, installed_apps=INSTALLED_APPS)
