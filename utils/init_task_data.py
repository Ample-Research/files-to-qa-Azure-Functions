import datetime
import uuid

from upload_to_table import upload_to_table

def init_task_data(task_id, config_data, file_size_in_bytes, filename, table_connection_str_secret):
    '''
    The goal of this function is to initialize the metadata for a new task (e.g. file-upload).
    It will take in the task_id and create a JSON dictionary that will track the task across its lifecycle.
    '''
    task_id = str(uuid.uuid4())

    task_id_meta_data = {
        # Azure Table Vars
        "PartitionKey": "tasks",
        "RowKey": task_id,
        # Core Meta Data
        "task_id": task_id,
        "raw_file_id": f"{task_id}_raw",
        "raw_text_id": f"{task_id}_txt",
        "final_output_id": f"{task_id}_final",
        # Processing Config
        "user_id": config_data.get("user_id"),
        "title": config_data.get("title"),
        "model_name": config_data.get("model_name", "qa-gpt-35-4k-context"),
        "start_sequence": config_data.get("start_sequence", "\n\n###\n\n"),
        "stop_sequence": config_data.get("stop_sequence", "###"),
        "task_type": config_data.get("task_type", "QA"),
        # Status Tracking
        "tags": [],
        "status": "initiated",
        "num_sections": 0.,
        "section_tracker": {},
        "date_created": str(datetime.datetime.now()),
        "error_message": None,
        "file_size_in_bytes": file_size_in_bytes,
        "filename": filename,
        "orchestrator_id": "",
        "download_link": ""
    }

    # Set empty task_type specific vars
    task_id_meta_data["custom_prompt_q"] = ""
    task_id_meta_data["custom_prompt_a"] = ""
    task_id_meta_data["num_QA_pairs"] = 0


    if task_id_meta_data["task_type"] == "QA":
        task_id_meta_data["custom_prompt_q"] = config_data.get("custom_prompt_q") # For Questions
        task_id_meta_data["custom_prompt_a"] = config_data.get("custom_prompt_a") # For Answers
        task_id_meta_data["num_QA_pairs"] = 0
    
    upload_to_table(task_id_meta_data, table_connection_str_secret, "tasks")

    return task_id_meta_data