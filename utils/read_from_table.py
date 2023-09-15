from azure.data.tables import TableClient
from utils.timeit import timeit

@timeit
def read_from_table(row_id, partition, table_name, table_connection_str_secret):
    table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name=table_name)
    entity = table_client.get_entity(partition_key=partition, row_key=row_id)
    return {k: entity[k] for k in entity.keys()}
