import importlib
import sys
from pathlib import Path


def get_project_root() -> Path:
    return Path.cwd()


def ensure_project_on_path() -> Path:
    root = get_project_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def load_main_module():
    ensure_project_on_path()
    return importlib.import_module("base.main")
