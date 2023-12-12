from pydantic.v1 import BaseModel, root_validator

from fastapi_jet.utils import name_fixer


class ProjectContext(BaseModel):
    name: str
    folder_name: str = None
    package_name: str = None
    use_templates: bool = False
    no_tests: bool = False

    @root_validator(pre=True)
    def set_folder_name(cls, values):
        if not values.get("folder_name"):
            values["folder_name"] = name_fixer(values["name"])
        return values

    @root_validator(pre=True)
    def set_package_name(cls, values):
        if not values.get("package_name"):
            values["package_name"] = name_fixer(values["name"], extra=["-"])
        return values


class AppContext(BaseModel):
    name: str
    folder_name: str

    @root_validator(pre=True)
    def validate_app(cls, values: dict):
        values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        return values


class AppRoute(dict):
    """
    AppRoute class to register routers
    """
    pass
