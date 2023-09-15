import logging

from azure.data.tables import TableClient
from utils.timeit import timeit

@timeit
def upload_to_table(data, table_connection_str_secret, table_name):
    try:
        table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name=table_name)
        table_client.create_entity(entity=data)
    except Exception as e:
        logging.error(f"Failed to upload to table: {e.status_code}")
        logging.error(e.message)

