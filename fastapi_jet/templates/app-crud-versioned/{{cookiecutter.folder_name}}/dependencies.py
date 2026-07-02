from .services import {{ cookiecutter.class_name }}Service


def get_{{ cookiecutter.module_name }}_service() -> {{ cookiecutter.class_name }}Service:
    return {{ cookiecutter.class_name }}Service()
