import hashlib
import os

from .db_util import DbUtil

CREATE_FILE_TABLE_QUERY = '''
    CREATE TABLE files (
    file_path TEXT NOT NULL,
    hash TEXT NOT NULL,
    archive_id INTEGER NOT NULL,
    PRIMARY KEY (file_path, hash),
    FOREIGN KEY (archive_id) REFERENCES archives(archive_id)
);
'''

CREATE_FILE_TABLE_INDEX_QUERY_0 = '''
    CREATE INDEX idx_file_hash ON files(hash);
'''

CREATE_FILE_TABLE_INDEX_QUERY_1 = '''
    CREATE INDEX idx_file_path ON files(file_path);
'''

CREATE_FILE_TABLE_INDEX_QUERY_2 = '''
    CREATE INDEX idx_file_archive ON files(archive_id);
'''

UPSERT_FILE_QUERY = '''
    INSERT INTO files (file_path, hash, archive_id)
    VALUES (?, ?, ?)
    ON CONFLICT(file_path, hash) DO UPDATE SET
        archive_id = excluded.archive_id;
'''

SEARCH_IF_FILE_ARCHIVED = '''
    SELECT COUNT(*) AS file_count FROM files WHERE file_path = '{0}' AND hash = '{1}'
'''


class FileTableDb:
    def __init__(self, db_util: DbUtil):
        self._db_util = db_util

    def create_table(self):
        self._db_util.update_commit(CREATE_FILE_TABLE_QUERY)
        self._db_util.update_commit(CREATE_FILE_TABLE_INDEX_QUERY_0)
        self._db_util.update_commit(CREATE_FILE_TABLE_INDEX_QUERY_1)
        self._db_util.update_commit(CREATE_FILE_TABLE_INDEX_QUERY_2)

    def is_file_archived(self, src_dir: str, file_path: str) -> tuple[str, bool]:
        dir_file_path = os.path.join(src_dir, file_path)
        file_hash = self.md5checksum(dir_file_path)
        escaped_path = file_path.replace("'", "''")
        escaped_hash = file_hash.replace("'", "''")
        count_query = SEARCH_IF_FILE_ARCHIVED.format(escaped_path, escaped_hash)
        result = self._db_util.query(count_query)
        count = result[0][0] if result else 0
        return file_hash, count > 0

    @staticmethod
    def md5checksum(file_name):
        md5 = hashlib.md5()

        # handle content in binary form
        f = open(file_name, "rb")

        while chunk := f.read(4096):
            md5.update(chunk)

        return md5.hexdigest()

    def __enter__(self):
        return self

    def __exit__(self):
        self._db_util.close()

    def upsert_file(self, file_path: str, archive_id: int, hash_value: str):
        self._db_util.update_commit(
            UPSERT_FILE_QUERY,
            (file_path, hash_value, archive_id),
        )
