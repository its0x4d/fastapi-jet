from fastapi import APIRouter

router = APIRouter()


@router.get("/", include_in_schema=False)
async def base_router() -> dict[str, str]:
    return {
        "message": "This is a base router for `{{cookiecutter.folder_name}}` app",
    }
