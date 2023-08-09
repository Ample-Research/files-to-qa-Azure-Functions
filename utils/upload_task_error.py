import json

from utils.upload_to_blob import upload_to_blob
from utils.read_from_blob import read_from_blob

def upload_task_error(task_id, function_name, error, blob_connection_str_secret):
    task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
    task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))
    task_id_meta["error_message"] = f"Error in {function_name}: {error}"
    task_id_meta["status"] = "error"
    upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret,"tasks-meta-data", task_id)