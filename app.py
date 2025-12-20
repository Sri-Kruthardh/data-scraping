import sys
from log_setup import log_setup
import logging

logger = logging.getLogger(__name__)
log_setup()

# bitcoin imports
# from src.bitcoin.bitcoin import run as bitcoin_run
# from src.databases.influx import insert_data_into_db

#entsoe imports
# from src.entsoe.sftp import run as entsoe_run
# from src.databases.sqlite3_setup import insert_data_sqlite

# books to scrape imports
from src.databases.sqlite3_connection import setup_catalogue_data
from src.web_scraping.bookstoscrape.scraper import scraper

def app():
    choice = sys.argv
    match choice[1]:
        # case 'bitcoin':
        #     datapoint = bitcoin_run()
        #     insert_data_into_db(datapoint)
        # case 'entsoe':
        #     data = entsoe_run()
        #     insert_data_sqlite(data)
        case 'bookstoscrape':
            setup_catalogue_data(scraper())



if __name__ == '__main__':
    log_setup()
    app()