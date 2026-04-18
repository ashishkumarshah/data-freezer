import os
import tarfile
import time
import hashlib

from .archive_table_db import ArchiveTableDb
from .archive_table_db import ArchiveStatus
from .file_table_db import FileTableDb
from .db_util import DbUtil
from .workspace_utils import FOLDER_NAME


class WorkspaceArchiver:
    def __init__(self, source_dir: str, workspace_dir: str):
        self.source_dir = source_dir
        self.workspace_dir = workspace_dir
        self.work_dir = os.path.join(self.workspace_dir, FOLDER_NAME)
        self.db_util = DbUtil(self.work_dir, False)
        self.files_db = FileTableDb(self.db_util)
        self.archives_db = ArchiveTableDb(self.db_util)

    def archive_workspace(self):
        epoch = int(time.time())
        paths = self.collect_files_for_archiving()
        if len(paths) == 0:
            print(f'No new files in {self.source_dir} to archive')
            return None
        self.archives_db.upsert_archive(archive_id=epoch, timestamp=epoch, status=ArchiveStatus.PREPARING,
                                        remote_key=None, checksum=None, size=0)
        for file_path, file_hash in paths:
            self.files_db.upsert_file(file_path=file_path, archive_id=epoch, hash_value=file_hash)
        archive_path = self.create_archive(paths, epoch)
        archive_size = os.path.getsize(archive_path)
        archive_checksum = self.md5checksum(archive_path)
        self.archives_db.upsert_archive(
            archive_id=epoch,
            timestamp=epoch,
            status=ArchiveStatus.PREPARED,
            remote_key=None,
            checksum=archive_checksum,
            size=archive_size,
        )
        return archive_path

    def collect_files_for_archiving(self):
        paths = []
        for root, _, files in os.walk(self.source_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, self.source_dir)
                hash_code, archived = self.files_db.is_file_archived(self.source_dir, relative_path)
                if not archived:
                    print(f'Collection {relative_path} for archiving')
                    paths.append([relative_path, hash_code])
                else:
                    print(f'Not archiving {relative_path}')
        return paths

    def create_archive(self, paths, epoch):
        archive_name = str(epoch) + '.tar.gz'
        archive_path = os.path.join(self.work_dir, archive_name)
        with tarfile.open(archive_path, "w:gz") as tar:
            for file_path, _ in paths:
                relative_path = os.path.join(self.source_dir, file_path)
                print(f'Archiving {relative_path}')
                tar.add(relative_path, arcname=file_path)
        return archive_path

    @staticmethod
    def md5checksum(file_name: str) -> str:
        md5 = hashlib.md5()
        with open(file_name, "rb") as file_handle:
            while chunk := file_handle.read(4096):
                md5.update(chunk)
        return md5.hexdigest()
