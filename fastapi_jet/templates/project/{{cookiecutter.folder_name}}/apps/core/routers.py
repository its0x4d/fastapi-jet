from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def core_index() -> dict[str, str]:
    return {"message": "Sample core app for {{ cookiecutter.name }}"}
