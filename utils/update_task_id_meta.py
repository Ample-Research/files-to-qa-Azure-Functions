from azure.data.tables import TableClient

def update_task_id_meta(task_id, updated_data, table_connection_str_secret):
    table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name="tasks")
    task_data = table_client.get_entity(partition_key="tasks", row_key=task_id)
    for key, value in updated_data.items():
        task_data[key] = value
    table_client.update_entity(mode="Merge", entity=task_data)


def increment_numerical_field(task_id, field_name, increment_value, table_connection_str_secret):
    table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name="tasks")
    task_data = table_client.get_entity(partition_key="tasks", row_key=task_id)
    if field_name in task_data:
        task_data[field_name] += increment_value
    else:
        task_data[field_name] = increment_value
    table_client.update_entity(mode="Merge", entity=task_data)


def append_tag_field(task_id, tag_list, table_connection_str_secret):
    table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name="tasks")
    task_data = table_client.get_entity(partition_key="tasks", row_key=task_id)
    existing_tags = task_data.get('tags', [])
    updated_tags = list(set(existing_tags + tag_list))
    task_data['tags'] = updated_tags
    table_client.update_entity(mode="Merge", entity=task_data)