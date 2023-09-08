import logging
import json
import time

from utils.upload_to_blob import upload_to_blob
from utils.read_from_blob import read_from_blob
from utils.update_task_id_meta import update_task_id_metadata
from utils.init_function import init_function
from utils.combine_qa import combine_qa
from utils.combine_chat import combine_chat

def main(inputData: dict) -> dict:
    '''
    COMBINE_SECTIONS will combined each section's JSONL into a single output file.
    It is triggered by SECTION_ORCHESTRATOR once each section is complete.
    This function performs three main tasks:
        1. Combines each section JSONL string into a single large JSONL file
        2. Validates and corrects the format
        2. Stores this final JSONL file inot a blob as the final result
        3. Updates Task_ID_Status (Task_ID) to mark processing as complete & gives it the Final File_ID
    '''
    try:
        start_time, blob_connection_str_secret, queue_connection_str_secret, error_msg = init_function("COMBINE_SECTIONS", "ACTION")

        task_id = inputData["task_id"]
        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))
        task_type = task_id_meta["task_type"]

        alreadyRun = task_id_meta["status"] == "completed"
        if alreadyRun: # Make function idempotent in case it double-fires
            logging.info(f'Task {task_id} has already been completed. Exiting COMBINE_SECTIONS.')
            {"task_id": task_id}

        if task_type == "QA":
            download_link = combine_qa(task_id_meta, blob_connection_str_secret)
        elif task_type == "CHAT":
            download_link = combine_chat()
        else: # Default to "QA"
            download_link = combine_qa(task_id_meta, blob_connection_str_secret)
        
        updates = {
            "download_link": download_link,
            "status": "completed"
        }
        update_task_id_metadata(task_id_meta, updates, blob_connection_str_secret)

        logging.info(f'COMBINE_SECTIONS function for task {task_id} successfully completed!')
        return {"task_id": task_id}

    except Exception as e:
        logging.error(f"Failed to combine sections in COMBINE_SECTIONS for task {task_id}: {str(e)}")
        task_id_meta["error_message"] = str(e)
        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret, "tasks-meta-data", task_id)
        raise e