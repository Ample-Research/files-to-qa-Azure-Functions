import json
import os
import logging

from utils.upload_to_blob import upload_to_blob
from utils.upload_to_table import upload_to_table
from utils.upload_to_queue import upload_to_queue
from utils.update_task_id_meta import update_task_id_meta
from utils.timeit import timeit

@timeit
def trigger_sections(sections, task_id, task_type, prompt_data, blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret):

  try:
    update_task_id_meta(task_id, {"num_sections": len(sections)}, table_connection_str_secret)

    for idx, section in enumerate(sections):
      this_section_id = f"{task_id}_section_{str(idx)}"
      upload_to_blob(section, blob_connection_str_secret,"file-sections", this_section_id)
      section_meta = {
        # Azure Table Vars
        "PartitionKey": task_id,
        "RowKey": this_section_id,
        # Core Meta Data
        "task_id": task_id,
        "status": "initiated"
      }

      queue_msg = {
        "section_id": this_section_id, 
        "task_id": task_id, 
        "prompt_data": prompt_data, 
        "task_type": task_type
      }
      upload_to_table(section_meta, table_connection_str_secret, "sections")
      upload_to_queue(json.dumps(queue_msg),queue_connection_str_secret, os.environ["PROCESS_SECTION_QUEUE"])

  except Exception as e:
    logging.error(f"Failed in Trigger Sections: {e}")
    raise e

  return True