# global module import
import json
import logging
from datetime import datetime
import requests

# set up logger
logger = logging.getLogger()

# config has all the constants needed to run the script
CONFIG = {
    'url': 'https://api.coindesk.com/v1/bpi/currentprice.json',
    'currency': 'USD',
    'date_format': '%Y-%m-%dT%H:%M:%S',
    'data_type': 'Time Series'
}


def run():
    """
    run method is common to all scrapers
    Gets data from the source and stores it
    into a database
    :return:
    """
    try:
        response = requests.get(
            url=CONFIG['url'],
            verify=False)
        if response.status_code == 200:
            logger.info(
                f'status_code: {response.status_code}. Message: {response.reason}'
            )
            data = json.loads(response.text)

            # get only datetime and not timezone
            date_time = data['time']['updatedISO'][:-6]
            date_time = datetime.strptime(date_time, CONFIG['date_format'])
            value = float(data['bpi'][CONFIG['currency']]['rate'].replace(',',''))
            logger.info(f'{date_time}: {value}')
            return date_time, value

        else:
            logger.error(f'Unexpected response received: {response.status_code} - {response.reason}')
    except Exception as e:
        logger.error(f'Unable to capture data due to reason: {e}')
        raise e