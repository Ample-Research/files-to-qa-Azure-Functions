import logging
import time

from utils.fetch_credentials import fetch_credentials
from utils.create_error_msg import create_error_msg
from utils.timeit import timeit

@timeit
def init_function(func_name, func_type):
    logging.info(f'{func_name} function initiated')
    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = fetch_credentials()
    except Exception as e:
        if func_type == "HTTP":
            error_msg = create_error_msg(e, note=f"Failed credentials in {func_name}")
        else:
            logging.error(f"Failed to connect credentials in {func_name}: {str(e)}")
            raise e
    return blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret