import os
from typing import Optional

from .db_util import DbUtil
from .archive_table_db import ArchiveTableDb
from .file_table_db import FileTableDb
from .workspace_archiver import WorkspaceArchiver
from .deepfreeze import DeepFreezeUtil
from .workspace_paths import resolve_workspace_dir, resolve_work_dir


def run_setup_command(source_dir: Optional[str] = None, work_dir: Optional[str] = None):
    _ = resolve_workspace_dir(source_dir)
    workspace_dir = resolve_workspace_dir(work_dir)
    setup_workspace(workspace_dir)


def run_archive_command(source_dir: Optional[str] = None, work_dir: Optional[str] = None):
    resolved_source_dir = resolve_workspace_dir(source_dir)
    workspace_dir = resolve_workspace_dir(work_dir)
    archive_path = archive_workspace(resolved_source_dir, workspace_dir)
    if archive_path is not None:
        print(f'Workspace archived at : {archive_path}')
        DeepFreezeUtil(archive_path).upload()


def archive_workspace(source_dir: str, workspace_dir: str):
    print(f'Workspace: {workspace_dir}...')
    print(f'Archiving files in {source_dir}...')
    archiver = WorkspaceArchiver(source_dir, workspace_dir)
    return archiver.archive_workspace()


def run_search_command(file_name_pattern: str, work_dir: Optional[str] = None):
    workspace_dir = resolve_workspace_dir(work_dir)
    print(f'Workspace: {workspace_dir}...')
    print(f'Searching metadata for files matching the pattern {file_name_pattern}...')


def run_restore_command(archive_id: str):
    print(f'Initiating Restore of Archive {archive_id}...')


def run_doctor_command(source_dir: Optional[str] = None, work_dir: Optional[str] = None):
    resolved_source_dir = resolve_workspace_dir(source_dir)
    workspace_dir = resolve_workspace_dir(work_dir)
    print(f'Workspace: {workspace_dir}...')
    print(f'Rescuing files from {resolved_source_dir}...')


def setup_workspace(workspace_dir: str):
    work_dir = _create_work_folder(workspace_dir)
    _initialize_db(work_dir)


def _create_work_folder(workspace_dir: str) -> str:
    work_dir = resolve_work_dir(workspace_dir)
    print(f'Creating working directory: {work_dir}')
    os.makedirs(work_dir, exist_ok=True)
    assert os.path.exists(work_dir)
    return work_dir


def _initialize_db(work_dir: str):
    assert os.path.exists(work_dir)
    with DbUtil(work_dir, True) as db:
        ArchiveTableDb(db).create_table()
        FileTableDb(db).create_table()
    print('Database initialization completed successfully')
