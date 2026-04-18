from pathlib import Path
import shutil

from data_freezer.utils.workspace_archiver import WorkspaceArchiver
from data_freezer.utils.workspace_utils import setup_workspace


def test_archive_workspace_archives_everything_new_workspace(capsys, tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    source_dir = repo_root / "test_data" / "source_dir"
    work_dir = tmp_path / "work_dir"

    setup_workspace(str(work_dir))

    archiver = WorkspaceArchiver(str(source_dir), str(work_dir))

    archiver.archive_workspace()
    output = capsys.readouterr().out

    expected_files = sorted(
        path.relative_to(source_dir).as_posix()
        for path in source_dir.rglob("*")
        if path.is_file()
    )

    for relative_path in expected_files:
        assert f"Collection {relative_path} for archiving" in output
        assert f"Archiving {source_dir / relative_path}" in output


def test_archive_workspace_archives_new_files_existing_workspace(capsys, tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    source_dir = repo_root / "test_data" / "source_dir"
    existing_workspace_fixture = repo_root / "test_data" / "work_dir" / "existing_workspace"
    work_dir = tmp_path / "existing_workspace"
    shutil.copytree(existing_workspace_fixture, work_dir)

    archiver = WorkspaceArchiver(str(source_dir), str(work_dir))

    archiver.archive_workspace()
    output = capsys.readouterr().out

    expected_new_files = sorted(
        path.relative_to(source_dir).as_posix()
        for path in source_dir.rglob("*")
        if path.is_file() and path.name.startswith("new.")
    )

    not_expected_files = sorted(
        path.relative_to(source_dir).as_posix()
        for path in source_dir.rglob("*")
        if path.is_file() and path.name.startswith("already.")
    )

    for relative_path in expected_new_files:
        assert f"Collection {relative_path} for archiving" in output
        assert f"Archiving {source_dir / relative_path}" in output

    for relative_path in not_expected_files:
        assert f"Not archiving {relative_path}" in output
