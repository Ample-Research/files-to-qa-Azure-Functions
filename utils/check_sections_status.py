from azure.data.tables import TableClient
from utils.timeit import timeit

@timeit
def check_sections_status(task_id, total_num_sections, table_connection_str_secret):
  table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name="sections")
  completed_sections = table_client.query_entities(query_filter="PartitionKey eq '{}' and status eq 'complete'".format(task_id))
  if len(completed_sections) == total_num_sections:
      return True
  else:
      return False

@timeit
def track_sections_completion(task_id, total_num_sections, table_connection_str_secret):
  table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name="sections")
  completed_sections = table_client.query_entities(query_filter="PartitionKey eq '{}' and status eq 'complete'".format(task_id))
  return len(completed_sections) / total_num_sections