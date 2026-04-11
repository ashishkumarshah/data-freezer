import os
import sys

import typer
from typing import Annotated, Optional
from data_freezer.utils.workspace_utils import setup_workspace


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
    print("Setting up data freezer...")
    if source_dir is None:
        source_dir = os.getcwd()
    if work_dir is None:
        work_dir = os.getcwd()

    setup_workspace(work_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python setup_command.py <source_dir> <work_dir>")
    command()
