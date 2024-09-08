import sys

# bitcoin imports
from src.web_scraping.bitcoin.bitcoin import run as bitcoin_run
from src.databases.influx import insert_data_into_db

#entsoe imports
from src.web_scraping.entsoe.sftp import run as entsoe_run
from src.databases.sqlite3_setup import insert_data_sqlite

from log_setup import log_setup


def app():
    choice = sys.argv
    match choice[1]:
        case 'bitcoin':
            datapoint = bitcoin_run()
            insert_data_into_db(datapoint)
        case 'entsoe':
            data = entsoe_run()
            insert_data_sqlite(data)



if __name__ == '__main__':
    log_setup()
    app()