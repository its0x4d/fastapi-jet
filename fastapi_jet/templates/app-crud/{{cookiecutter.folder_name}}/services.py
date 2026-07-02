from .schemas import {{ cookiecutter.class_name }}Create, {{ cookiecutter.class_name }}Read, {{ cookiecutter.class_name }}Update


class {{ cookiecutter.class_name }}Service:
    """Business logic for the {{ cookiecutter.folder_name }} app."""

    def list(self) -> list[{{ cookiecutter.class_name }}Read]:
        return []

    def get(self, item_id: int) -> {{ cookiecutter.class_name }}Read:
        return {{ cookiecutter.class_name }}Read(id=item_id, name="example")

    def create(self, payload: {{ cookiecutter.class_name }}Create) -> {{ cookiecutter.class_name }}Read:
        return {{ cookiecutter.class_name }}Read(id=1, name=payload.name)

    def update(
        self, item_id: int, payload: {{ cookiecutter.class_name }}Update
    ) -> {{ cookiecutter.class_name }}Read:
        return {{ cookiecutter.class_name }}Read(id=item_id, name=payload.name or "example")

    def delete(self, item_id: int) -> None:
        return None
