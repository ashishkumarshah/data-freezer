import os
import sys

import typer
from typing import Annotated, Optional


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
    print(f'Workspace: {work_dir}...')
    print(f'Archiving files in {source_dir}...')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python archive_command.py <source_dir> <work_dir>")
    command(sys.argv[1], sys.argv[2])
