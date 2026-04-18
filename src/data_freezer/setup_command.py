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
    source_dir = source_dir or os.getcwd()
    work_dir = work_dir or os.getcwd()

    assert source_dir is not None
    assert work_dir is not None

    setup_workspace(work_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python setup_command.py <source_dir> <work_dir>")
    command()
