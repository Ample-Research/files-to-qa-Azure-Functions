import datetime

def init_task_data(task_id, config_data, file_size_in_bytes, filename):
    '''
    The goal of this function is to initialize the metadata for a new task (e.g. file-upload).
    It will take in the task_id and create a JSON dictionary that will track the task across its lifecycle.
    '''

    task_id_meta_data = {
        # Core Meta Data
        "task_id": task_id,
        "raw_file_id": f"{task_id}_raw",
        "raw_text_id": f"{task_id}_txt",
        "final_output_id": f"{task_id}_final",
        # Processing Config
        "user_id": config_data.get("user_id"),
        "title": config_data.get("title"),
        "custom_prompt_q": config_data.get("custom_prompt_q"), # For Questions
        "custom_prompt_a": config_data.get("custom_prompt_a"), # For Answers
        "model_name": config_data.get("model_name", "qa-gpt-35-4k-context"),
        "start_sequence": config_data.get("start_sequence", "\n\n###\n\n"),
        "stop_sequence": config_data.get("stop_sequence", "###"),
        "process_type": config_data.get("process_type", "QA"),
        # Status Tracking
        "tags": [],
        "status": "initiated",
        "section_tracker": {},
        "date_created": str(datetime.datetime.now()),
        "error_message": None,
        "num_QA_pairs": 0,
        "processing_time": 0,
        "file_size_in_bytes": file_size_in_bytes,
        "filename": filename,
        "orchestrator_id": ""
    }
    
    return task_id_meta_data
