import typer
import sys
from typing import Annotated

from .utils.workspace_utils import run_restore_command


def command(
        archive_id: Annotated[str, typer.Option(help="Archive ID")],
):
    run_restore_command(archive_id)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        sys.exit("Usage: python restore_command.py archive_id")
    command(sys.argv[1])
