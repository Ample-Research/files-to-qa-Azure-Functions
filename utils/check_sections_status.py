from azure.data.tables import TableClient
from utils.timeit import timeit

@timeit
def check_sections_status(task_id, total_num_sections, table_connection_str_secret):
  table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name="sections")
  completed_sections = table_client.query_entities(query_filter="PartitionKey eq '{}' and (status eq 'complete' or status eq 'failed')".format(task_id))

  count = 0
  for _ in completed_sections:
    count += 1

  if count == total_num_sections:
      return True
  else:
      return False

@timeit
def track_sections_completion(task_id, total_num_sections, status, table_connection_str_secret):

  if status == "complete":
    return 1

  if status != "section_processing_triggered":
    return 0
  
  table_client = TableClient.from_connection_string(table_connection_str_secret.value, table_name="sections")
  completed_sections = table_client.query_entities(query_filter="PartitionKey eq '{}' and (status eq 'complete' or status eq 'failed')".format(task_id))

  count = 0
  for _ in completed_sections:
    count += 1

  return count / total_num_sections