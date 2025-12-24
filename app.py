import sys
from log_setup import log_setup
import logging

logger = logging.getLogger(__name__)

# bitcoin imports
# from src.bitcoin.bitcoin import run as bitcoin_run
# from src.databases.influx import insert_data_into_db

#entsoe imports
# from src.entsoe.sftp import run as entsoe_run
# from src.databases.sqlite3_setup import insert_data_sqlite

# books to scrape imports
from src.databases.sqlite3_connection import setup_catalogue_data
from src.web_scraping.bookstoscrape.scraper import scraper, genre_scraper

def app():
    logger.info("Starting web scraping application..")
    choice = sys.argv
    match choice[1]:
        # case 'bitcoin':
        #     datapoint = bitcoin_run()
        #     insert_data_into_db(datapoint)
        # case 'entsoe':
        #     data = entsoe_run()
        #     insert_data_sqlite(data)
        case 'bookstoscrape':
            logger.info("Choice selected: bookstoscrape")
            if choice[2] == 'catalogue':
                logger.info("Proceeding to scrape list of catalogues..")
                setup_catalogue_data(scraper())
            elif choice[2] == 'genre':
                if choice[3]:
                    genre_scraper(choice[3])
                    logger.info(f"Proceeding to scrape genre specific data. Selected genre: {choice[3]}")

                else:
                    logger.warning("No genre is specified. Proceeding to scrape all genres")


if __name__ == '__main__':
    log_setup()
    app()