import os
from enum import Enum
from typing import List
import questionary


def enum_question(choices: Enum) -> questionary.Question:
    """
    This function is used to present a question with multiple choices to the user.

    :param choices: An enumeration type that contains the possible choices.
    :type choices: EnumType
    :return: A questionary.Question object, which can be used to interactively ask the user a question.
    :rtype: questionary.Question
    """
    return questionary.select(
        "Select a choice:",
        choices=[choice.value for choice in choices],
    )


def binary_question(question: str, default: bool = False) -> questionary.Question:
    """
    This function is used to present a binary question (yes/no) to the user.

    :param question: The question to ask the user.
    :type question: str
    :param default: The default answer to the question. If not provided, the default is False (no).
    :type default: bool, optional
    :return: A questionary.Question object, which can be used to interactively ask the user a question.
    :rtype: questionary.Question
    """
    return questionary.confirm(
        question,
        default=default,
    )


def name_fixer(name: str, extra: List[str] = None) -> str:
    """
    This function is used to replace certain special characters in a string with an underscore.

    :param name: The original string that needs to be fixed.
    :type name: str
    :param extra: An optional list of additional characters that should be replaced.
    :type extra: List[str], optional
    :return: The fixed string.
    :rtype: str
    """
    # Define the default list of characters to replace.
    chars = "* /\\|<>?:\"' "

    # If the 'extra' parameter is provided, add its characters to the list of characters to replace.
    if extra:
        chars += "".join(extra)

    # Replace each character in the list with an underscore.
    for char in chars:
        name = name.replace(char, "_")

    return name


def is_fastapi_project() -> bool:
    """
    This function is used to check if the current project is a FastAPI project.

    It does this by checking if a specific file ('base/main.py') exists in the current working directory.
    The assumption is that a FastAPI project would have this file in the 'base' directory.

    :return: A boolean indicating if the current project is a FastAPI project.
    :rtype: bool
    """
    # Construct the path to the 'base/main.py' file in the current working directory.
    fastapi_main_path = os.path.join(os.getcwd(), 'base', 'main.py')
    return os.path.exists(fastapi_main_path)
