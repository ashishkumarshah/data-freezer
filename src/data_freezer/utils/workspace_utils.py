import os
import sqlite3

FOLDER_NAME = ".data_freeze"
DB_NAME = "data_freeze.sqlite"
CREATE_ARCHIVE_TABLE_QUERY = '''
    CREATE TABLE archives (
    archive_id TEXT PRIMARY KEY,
    timestamp INTEGER NOT NULL,
    remote_key TEXT,
    checksum TEXT,
    size INTEGER,
    status TEXT NOT NULL CHECK (
        status IN ('PREPARING', 'PREPARED', 'UPLOADED', 'FAILED', 'NODATA')
    )
);
    '''
CREATE_ARCHIVE_TABLE_INDEX_QUERY = '''
    CREATE INDEX idx_archive_status ON archives(status);
'''

CREATE_FILE_TABLE_QUERY = '''
    CREATE TABLE files (
    file_path TEXT NOT NULL,
    hash TEXT NOT NULL,
    archive_id TEXT,
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


def setup_workspace(work_dir_path: str):
    work_dir = _create_work_folder(work_dir_path)
    _initialize_db(work_dir)


def _create_work_folder(work_dir_path: str) -> str:
    work_dir = os.path.join(work_dir_path, FOLDER_NAME)
    print(f'Creating working directory: {work_dir}')

    os.makedirs(work_dir, exist_ok=True)

    assert os.path.exists(work_dir)
    return work_dir


def _initialize_db(work_dir: str):
    assert os.path.exists(work_dir)

    db_path = os.path.join(work_dir, DB_NAME)

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        print(f'Connected to database: {db_path}')

        cursor.execute(CREATE_ARCHIVE_TABLE_QUERY)
        cursor.execute(CREATE_ARCHIVE_TABLE_INDEX_QUERY)
        cursor.execute(CREATE_FILE_TABLE_QUERY)
        cursor.execute(CREATE_FILE_TABLE_INDEX_QUERY_0)
        cursor.execute(CREATE_FILE_TABLE_INDEX_QUERY_1)
        cursor.execute(CREATE_FILE_TABLE_INDEX_QUERY_2)

        connection.commit()
        print(f'Database initialization completed successfully')
