from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index() -> dict[str, str]:
    return {
        "message": "Versioned {{ cookiecutter.folder_name }} app",
        "version": "v1",
    }
