import os
import sqlite3
from typing import Any, Sequence

DB_NAME = "data_freeze.sqlite"


class DbUtil:
    def __init__(self, workspace_dir: str, create_db: bool):
        self.workspace_dir = workspace_dir
        self.DB_PATH = os.path.join(self.workspace_dir, DB_NAME)
        abs_db_path = os.path.abspath(self.DB_PATH)
        if not create_db:
            assert os.path.exists(abs_db_path), f"DB file not found: {abs_db_path}"
        self.conn = sqlite3.connect(self.DB_PATH)
        assert os.path.exists(abs_db_path), f"DB file not found: {abs_db_path}"

    def update_commit(self, query: str, params: Sequence[Any] = ()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()

    def query(self, query: str, params: Sequence[Any] = ()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
