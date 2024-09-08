import sqlite3
import os
import logging
from datetime import datetime
logger = logging.getLogger()

def connect():
    logger.info('Connecting to database locally')
    connection = sqlite3.connect(os.environ.get('sql3_path'))
    cursor = connection.cursor()
    return cursor,connection

def insert_data(data,cursor):
    date_format = '%Y-%m-%d %H:%M'
    logger.info('Inserting data into the database')
    count = 0
    for row in data:
        q =  f"""
            insert into intraday_capacity (delivery_date, resolution_code,
            allocation_id,allocation_mode_code,
            capacity_product_code,
            out_area_code, out_area_type_code,
            out_area_name, out_area_code, 
            out_area_type_code, out_area_name,
            capacity, update_datetime)
            values("{datetime.strptime(row['DateTime'],date_format)}", "{row['ResolutionCode']}", 
            "{row['AllocationId']}", "{row['AllocationModeCode']}",
            "{row['CapacityProductCode']}",
            "{row['OutAreaCode']}", "{row['OutAreaTypeCode']}",
            "{row['OutAreaName']}", "{row['InAreaCode']}",
            "{row['InAreaTypeCode']}", "{row['InAreaName']}",
            "{row['Capacity']}", "{datetime.strptime(row['UpdateTime'],date_format)}")
            """
        cursor.execute(q)
        count += 1
    logger.info(f'{count} rows inserted successfully')

def insert_data_sqlite(data):
    cursor,connection = connect()
    insert_data(data, cursor)
    connection.commit()
    cursor.close()