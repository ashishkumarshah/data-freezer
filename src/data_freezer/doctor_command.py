import sys

import typer
from typing import Annotated, Optional
from .utils.workspace_utils import run_doctor_command


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
    run_doctor_command(source_dir=source_dir, work_dir=work_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python doctor_command.py <source_dir> <work_dir>")
    command(sys.argv[1], sys.argv[2])
