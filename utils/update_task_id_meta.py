import json
from utils.upload_to_blob import upload_to_blob

def update_task_id_metadata(current_metadata, updates, blob_connection_str_secret):
    
    for key, value in updates.items():
      
      if key == "single_section":
        current_metadata["section_tracker"][value["section_id"]] = value["status"]
      elif key == "tags":
         current_metadata["tags"] = list(set(current_metadata["tags"] + value))
      elif key == "num_QA_pairs":
         current_metadata["num_QA_pairs"] += value
      else:
        current_metadata[key] = value

    upload_to_blob(json.dumps(current_metadata), blob_connection_str_secret, "tasks-meta-data", current_metadata["task_id"])
    return current_metadata