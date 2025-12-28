import sqlite3
import logging
import os

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

def create_books_table(cursor):
    q = f"""
        CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        price TEXT NOT NULL,
        availability TEXT NOT NULL,
        rating INTEGER,
        book_detail_url TEXT NOT NULL
        );
        """
    cursor.execute(q)
    logger.info('books table created if it doesnt exist')

def insert_catalogue_data(rows, cursor):
    rows = [(k,v) for k,v in rows.items()]
    q = f"""
        INSERT INTO book_catalogue (name,url) VALUES (?, ?)
        ON CONFLICT DO NOTHING
        """
    result = cursor.executemany(q,rows)
    logger.info(f'inserted {result.rowcount} rows into the table...')

def insert_books_data(cursor, data):
    rows = [(i['name'], i['price'], i['availability'], i['rating'], i['book_detail_url']) for i in data]
    q = f"""
        INSERT INTO books (name,price,availability,rating,book_detail_url) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT DO NOTHING
        """
    result = cursor.executemany(q,rows)
    logger.info(f'inserted {result.rowcount} rows into the table...')


def setup_catalogue_data(data):
    with SQLiteConnection() as db:
        cursor = db.cursor()
        create_catalogue_table(cursor)
        insert_catalogue_data(data,cursor)

def get_genre_data(genre):
    q = f"""
    SELECT name, url FROM book_catalogue where name = '{genre}'
    """
    with SQLiteConnection() as db:
        cur = db.cursor()
        result = cur.execute(q).fetchall()
        if result:
            return result
        else:
            logger.warning(f"Genre {genre} does not exist.")
            return

def get_all_genres():
    q = f"""
    SELECT name, url FROM book_catalogue
    """
    with SQLiteConnection() as db:
        cur = db.cursor()
        result = cur.execute(q).fetchall()
        if result:
            return result
        else:
            logger.warning(f"Data missing from book_catalogue table")
            return


def save_books_data(li):
    with SQLiteConnection() as db:
        cursor = db.cursor()
        create_books_table(cursor)
        insert_books_data(cursor, li)