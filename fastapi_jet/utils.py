from enum import Enum
from pathlib import Path

import questionary

_DEFAULT_BAD_CHARS = "* /\\|<>?:\"' "
_DEFAULT_NAME_TABLE = str.maketrans({char: "_" for char in _DEFAULT_BAD_CHARS})


def enum_question(choices: Enum) -> questionary.Question:
    """Return a select prompt for the given enum choices."""
    return questionary.select(
        "Select a choice:",
        choices=[choice.value for choice in choices],
    )


def binary_question(question: str, default: bool = False) -> questionary.Question:
    """Return a yes/no confirmation prompt."""
    return questionary.confirm(question, default=default)


def name_fixer(name: str, extra: list[str] | None = None) -> str:
    """Replace filesystem-unsafe characters with underscores."""
    if not extra:
        return name.translate(_DEFAULT_NAME_TABLE)
    table = str.maketrans(
        {char: "_" for char in _DEFAULT_BAD_CHARS + "".join(extra)}
    )
    return name.translate(table)


def is_fastapi_project() -> bool:
    """Return True when the current directory is a fastapi-jet project."""
    root = Path.cwd()
    if (root / ".fastapi-jet").is_file():
        return True
    if (root / "pyproject.toml").is_file():
        content = (root / "pyproject.toml").read_text(encoding="utf-8")
        if "[tool.fastapi-jet]" in content and (root / "base" / "main.py").is_file():
            return True
    return (root / "base" / "main.py").is_file()
