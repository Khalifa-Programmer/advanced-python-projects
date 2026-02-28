from services.api_service import fetch_data
from services.data_processor import insert_data
from database.mysql_connection import create_table
from utils.logger import setup_logging
import logging

if __name__ == "__main__":
    setup_logging()
    try:
        create_table()
    except Exception as e:
        logging.error(str(e))
        print("Database error: Unable to connect or create table.\nDetails:", e)
        exit(1)
    try:
        data = fetch_data()
    except Exception as e:
        logging.error(str(e))
        print("Network/API error: Unable to fetch data.\nDetails:", e)
        exit(1)
    try:
        insert_data(data)
        print("Data inserted successfully")
    except Exception as e:
        logging.error(str(e))
        print("Database error: Unable to insert data.\nDetails:", e)
        exit(1)
