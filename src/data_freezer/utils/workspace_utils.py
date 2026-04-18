import os

FOLDER_NAME = ".data_freeze"

from .db_util import DbUtil
from .archive_table_db import ArchiveTableDb
from .file_table_db import FileTableDb


def setup_workspace(work_dir_path: str):
    work_dir = _create_work_folder(work_dir_path)
    _initialize_db(work_dir)


def _create_work_folder(work_dir_path: str) -> str:
    work_dir = os.path.join(work_dir_path, FOLDER_NAME)
    print(f'Creating working directory: {work_dir}')

    os.makedirs(work_dir, exist_ok=True)

    assert os.path.exists(work_dir)
    return work_dir


def _initialize_db(work_dir: str):
    assert os.path.exists(work_dir)
    with DbUtil(work_dir, True) as db:
        ArchiveTableDb(db).create_table()
        FileTableDb(db).create_table()
    print(f'Database initialization completed successfully')
