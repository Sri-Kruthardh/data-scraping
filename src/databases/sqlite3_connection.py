import sqlite3
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class SQLiteConnection:
    def __init__(self):
        # setting isolation level to None to ensure auto commit
        self.connection = sqlite3.connect(os.environ.get('sql3_path'), isolation_level=None)

    def __enter__(self):
        logger.info('Connecting to database locally')
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.connection.close()
            logger.info('Connection closed.')

def create_catalogue_table(cursor):
    q = f"""
        CREATE TABLE IF NOT EXISTS book_catalogue(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        url TEXT NOT NULL UNIQUE);
        """
    cursor.execute(q)
    logger.info('book_catalogue table created if it doesnt exist')

def insert_catalogue_data(rows, cursor):
    rows = [(k,v) for k,v in rows.items()]
    q = f"""
        INSERT INTO book_catalogue (name,url) VALUES (?, ?)
        ON CONFLICT DO NOTHING
        """
    result = cursor.executemany(q,rows)
    logger.info(f'inserted {result.rowcount} rows into the table...')


def setup_catalogue_data(data):
    with SQLiteConnection() as db:
        cursor = db.cursor()
        create_catalogue_table(cursor)
        insert_catalogue_data(data,cursor)
