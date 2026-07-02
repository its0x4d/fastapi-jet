from fastapi import APIRouter, Depends, status

from .dependencies import get_{{ cookiecutter.module_name }}_service
from .schemas import (
    {{ cookiecutter.class_name }}Create,
    {{ cookiecutter.class_name }}Read,
    {{ cookiecutter.class_name }}Update,
)
from .services import {{ cookiecutter.class_name }}Service

router = APIRouter()


@router.get("/", response_model=list[{{ cookiecutter.class_name }}Read])
async def list_items(
    service: {{ cookiecutter.class_name }}Service = Depends(get_{{ cookiecutter.module_name }}_service),
) -> list[{{ cookiecutter.class_name }}Read]:
    return service.list()


@router.post(
    "/",
    response_model={{ cookiecutter.class_name }}Read,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(
    payload: {{ cookiecutter.class_name }}Create,
    service: {{ cookiecutter.class_name }}Service = Depends(get_{{ cookiecutter.module_name }}_service),
) -> {{ cookiecutter.class_name }}Read:
    return service.create(payload)


@router.get("/{item_id}", response_model={{ cookiecutter.class_name }}Read)
async def get_item(
    item_id: int,
    service: {{ cookiecutter.class_name }}Service = Depends(get_{{ cookiecutter.module_name }}_service),
) -> {{ cookiecutter.class_name }}Read:
    return service.get(item_id)


@router.patch("/{item_id}", response_model={{ cookiecutter.class_name }}Read)
async def update_item(
    item_id: int,
    payload: {{ cookiecutter.class_name }}Update,
    service: {{ cookiecutter.class_name }}Service = Depends(get_{{ cookiecutter.module_name }}_service),
) -> {{ cookiecutter.class_name }}Read:
    return service.update(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    service: {{ cookiecutter.class_name }}Service = Depends(get_{{ cookiecutter.module_name }}_service),
) -> None:
    service.delete(item_id)
