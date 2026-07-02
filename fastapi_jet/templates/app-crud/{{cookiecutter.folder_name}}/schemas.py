from pydantic import BaseModel


class {{ cookiecutter.class_name }}Create(BaseModel):
    name: str


class {{ cookiecutter.class_name }}Update(BaseModel):
    name: str | None = None


class {{ cookiecutter.class_name }}Read(BaseModel):
    id: int
    name: str
