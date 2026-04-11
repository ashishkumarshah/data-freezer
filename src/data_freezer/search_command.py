import os
import sys

import typer
from typing import Annotated, Optional


def command(
        file_name_pattern: Annotated[str, typer.Option("--pattern", "-p", help="File name pattern")],
        work_dir: Annotated[
            Optional[str],
            typer.Option(
                "--work-dir",
                "-w",
                help="Directory used for intermediate processing and metadata storage"
            )
        ] = None
):
    if work_dir is None:
        work_dir = os.getcwd()
    print(f'Workspace: {work_dir}...')
    print(f'Searching metadata for files matching the pattern {file_name_pattern}...')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python search_command.py <file_name_pattern> <work_dir>")
    command(sys.argv[1], sys.argv[2])
