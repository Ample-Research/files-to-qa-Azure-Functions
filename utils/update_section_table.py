from azure.data.tables import TableClient

def update_section_table(section_id, task_id, updated_data, table_connection_str_secret):
    table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name="sections")
    task_data = table_client.get_entity(partition_key=task_id, row_key=section_id)
    for key, value in updated_data.items():
        task_data[key] = value
    table_client.update_entity(mode="Merge", entity=task_data)


