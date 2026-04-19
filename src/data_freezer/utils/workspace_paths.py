import os
from typing import Optional

FOLDER_NAME = ".data_freeze"


def resolve_workspace_dir(path: Optional[str]) -> str:
    return path or os.getcwd()


def resolve_work_dir(workspace_dir: str) -> str:
    return os.path.join(workspace_dir, FOLDER_NAME)
