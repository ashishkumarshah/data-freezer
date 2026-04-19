import sys

import typer
from typing import Annotated, Optional
from .utils.workspace_utils import run_search_command


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
    run_search_command(file_name_pattern=file_name_pattern, work_dir=work_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python search_command.py <file_name_pattern> <work_dir>")
    command(sys.argv[1], sys.argv[2])
