from pydantic import BaseModel, model_validator

from fastapi_jet.app_registry import to_class_name
from fastapi_jet.utils import name_fixer


class ProjectContext(BaseModel):
    name: str
    folder_name: str | None = None
    package_name: str | None = None
    use_templates: bool = False
    no_tests: bool = False

    @model_validator(mode="before")
    @classmethod
    def set_derived_names(cls, values: dict) -> dict:
        if not values.get("folder_name"):
            values["folder_name"] = name_fixer(values["name"])
        if not values.get("package_name"):
            values["package_name"] = name_fixer(values["name"], extra=["-"])
        return values


class AppContext(BaseModel):
    name: str
    folder_name: str = ""
    module_name: str = ""
    class_name: str = ""
    crud: bool = False
    versioned: bool = False

    @model_validator(mode="before")
    @classmethod
    def normalize_app_name(cls, values: dict) -> dict:
        folder_name = values["name"].lower().replace(" ", "-").strip()
        values["folder_name"] = folder_name
        values["module_name"] = folder_name.replace("-", "_")
        values["class_name"] = to_class_name(folder_name)
        return values
