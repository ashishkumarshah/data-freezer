import os
import sys

import typer
from typing import Annotated, Optional

from .utils.workspace_archiver import WorkspaceArchiver
from .utils.deepfreeze import DeepFreezeUtil


def command(
        source_dir: Annotated[
            Optional[str],
            typer.Option(
                "--source-dir",
                "-s",
                help="Path to the source directory containing files to archive"
            )
        ] = None,
        work_dir: Annotated[
            Optional[str],
            typer.Option(
                "--work-dir",
                "-w",
                help="Directory used for intermediate processing and metadata storage"
            )
        ] = None,
):
    if source_dir is None:
        source_dir = os.getcwd()
    if work_dir is None:
        work_dir = os.getcwd()
    assert source_dir is not None
    assert work_dir is not None
    print(f'Workspace: {work_dir}...')
    print(f'Archiving files in {source_dir}...')
    archiver = WorkspaceArchiver(source_dir, work_dir)
    archive_path = archiver.archive_workspace()
    if archive_path is not None:
        print(f'Workspace archived at : {archive_path}')
        DeepFreezeUtil(archive_path).upload()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python archive_command.py <source_dir> <work_dir>")
    command(sys.argv[1], sys.argv[2])
