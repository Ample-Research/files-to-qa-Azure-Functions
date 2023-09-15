from azure.data.tables import TableClient

def upload_to_table(file_data, table_connection_str_secret, table_name, data):
    table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name=table_name)
    table_client.create_entity(entity=data)
