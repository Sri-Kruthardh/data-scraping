from src.web_scraping.bitcoin.bitcoin import run
from src.databases.influx import insert_data_into_db
from log_setup import log_setup


def app():
    datapoint = run()
    insert_data_into_db(datapoint)


if __name__ == '__main__':
    log_setup()
    app()