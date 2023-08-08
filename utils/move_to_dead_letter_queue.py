import json
import logging

from utils.upload_to_queue import upload_to_queue
from utils.upload_to_blob import upload_to_blob

def move_to_dead_letter_queue(queue_msg, task_id_meta, func_name, queue_connection_str_secret, blob_connection_str_secret, dq_threshold):
      dequeue_count = queue_msg.dequeue_count
      if dequeue_count > dq_threshold:
          error_msg = f"AUDIT: {task_id_meta['task_id']} moved to dead-letter-queue during {func_name}"
          logging.info(error_msg)
          task_id_meta["error_message"] = error_msg
          task_id = task_id_meta["task_id"]
          upload_to_queue(json.dumps(task_id_meta),queue_connection_str_secret,"dead-letter-queue")
          upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret,"tasks-meta-data", task_id)
          return True
      else:
           return False
