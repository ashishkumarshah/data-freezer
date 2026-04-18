from enum import Enum

from .db_util import DbUtil

class ArchiveStatus(str, Enum):
    PREPARING = "PREPARING"
    PREPARED = "PREPARED"
    UPLOADED = "UPLOADED"
    FAILED = "FAILED"
    NODATA = "NODATA"

ARCHIVE_STATUS_VALUES = ", ".join(f"'{status.value}'" for status in ArchiveStatus)

CREATE_ARCHIVE_TABLE_QUERY = '''
    CREATE TABLE archives (
    archive_id INTEGER PRIMARY KEY,
    timestamp INTEGER NOT NULL,
    remote_key TEXT,
    checksum TEXT,
    size INTEGER,
    status TEXT NOT NULL CHECK (
        status IN ({0})
    )
);
    '''.format(ARCHIVE_STATUS_VALUES)

CREATE_ARCHIVE_TABLE_INDEX_QUERY = '''
    CREATE INDEX idx_archive_status ON archives(status);
'''

UPSERT_ARCHIVE_QUERY = '''
    INSERT INTO archives (archive_id, timestamp, remote_key, checksum, size, status)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(archive_id) DO UPDATE SET
        timestamp = excluded.timestamp,
        remote_key = excluded.remote_key,
        checksum = excluded.checksum,
        size = excluded.size,
        status = excluded.status;
'''


class ArchiveTableDb:
    def __init__(self, db_util: DbUtil):
        self._db_util = db_util

    def create_table(self):
        self._db_util.update_commit(CREATE_ARCHIVE_TABLE_QUERY)
        self._db_util.update_commit(CREATE_ARCHIVE_TABLE_INDEX_QUERY)

    def upsert_archive(
        self,
        archive_id: int,
        timestamp: int,
        remote_key: str | None,
        checksum: str | None,
        size: int | None,
        status: ArchiveStatus,
    ):
        self._db_util.update_commit(
            UPSERT_ARCHIVE_QUERY,
            (archive_id, timestamp, remote_key, checksum, size, status.value),
        )
