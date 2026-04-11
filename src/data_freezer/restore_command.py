import typer
import sys
from typing import Annotated, Optional


def command(
        archive_id: Annotated[str, typer.Option(help="Archive ID")],
):
    print(f'Initiating Restore of Archive {archive_id}...')


if __name__ == "__main__":
    if len(sys.argv) < 1:
        sys.exit("Usage: python restore_command.py archive_id")
    command(sys.argv[1])
