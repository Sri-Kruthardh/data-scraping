import influxdb_client
import os
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
logger = logging.getLogger()


BUCKET = os.environ.get('bucket')
ORG = os.environ.get('org')
TOKEN = os.environ.get('token')
HOST = os.environ.get('influx_host')

#Create a new client instance
def init_client():
    logger.info('Initializing Influx db client')
    client = influxdb_client.InfluxDBClient(
        url=HOST,
        token=TOKEN,
        org=ORG
    )
    return client


def insert_data_into_db(measurement):
    logger.info('Inserting data in to the db')
    point = influxdb_client.Point(measurement_name='bitcoin_rate').field(measurement[0],measurement[1])
    client = init_client()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET,record=point)
    client.close()
    logger.info('Data saved into database')
