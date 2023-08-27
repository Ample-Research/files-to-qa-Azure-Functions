import json
from utils.upload_to_blob import upload_to_blob

def update_task_id_metadata(current_metadata, updates, blob_connection_str_secret):
    for key, value in updates.items():
      current_metadata[key] = value
    upload_to_blob(json.dumps(current_metadata), blob_connection_str_secret, "tasks-meta-data", current_metadata["task_id"])
    return current_metadata