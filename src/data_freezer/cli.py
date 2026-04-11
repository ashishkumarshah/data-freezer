import typer

from data_freezer.setup_command import command as setup_command
from data_freezer.archive_command import command as archive_command
from data_freezer.search_command import command as search_command
from data_freezer.restore_command import command as restore_command
from data_freezer.doctor_command import command as doctor_command

cli = typer.Typer(help="Data Freezer CLI for AWS Glacier operations", no_args_is_help=True)

cli.command(name="setup", help="Setup Data Freeze")(setup_command)
cli.command(name="search", help="Search for an archived file")(search_command)
cli.command(name="restore", help="Initiate restore of an archive")(restore_command)
cli.command(name="archive", help="Archive the source directory")(archive_command)
cli.command(name="doctor", help="Troubleshoot the current archival process")(doctor_command)


def main():
    cli(prog_name="data-freezer")


if __name__ == "__main__":
    main()
