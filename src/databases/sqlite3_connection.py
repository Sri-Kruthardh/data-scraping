import sqlite3
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class SQLiteConnection:
    def __enter__(self):
        logger.info('Connecting to database locally')
        # setting isolation level to None to ensure auto commit
        self.connection = sqlite3.connect(os.environ.get('sql3_path'), isolation_level=None)
        self.cursor = self.connection.cursor()
        return self.cursor, self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.cursor.close()
            logger.info("Cursor closed. Closing connection...")
            self.connection.close()
            logger.info('Connection closed.')

    def create_catalogue_table(self):
        q = f"""
            CREATE TABLE book_catalogue IF NOT EXISTS (
            id INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            url TEXT NOT NULL UNIQUE,
            insert_date TEXT NOT NULL);
            """
        self.cursor.execute(q)

    def insert_catalogue_data(self, rows):
        now = datetime.now(tz=timezone.utc)
        rows = [i.update({'insert_date': now}) for i in rows]
        q = f"""
            INSERT INTO book_catalogue (name,url,insert_date) VALUES (?, ?, ?)
            """
        self.cursor.executemany(q,rows)
        logger.info(f'inserted {len(rows)} rows into the table...')
