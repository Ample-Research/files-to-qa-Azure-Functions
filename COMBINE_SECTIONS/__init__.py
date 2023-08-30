import logging
import json
import time

from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.read_from_blob import read_from_blob
from utils.generate_blob_download_link import generate_blob_download_link
from utils.generate_valid_filename import generate_valid_filename
from utils.update_task_id_meta import update_task_id_metadata
from utils.combine_JSONL import combine_JSONL
from utils.init_function import init_function

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

        alreadyRun = task_id_meta["status"] == "completed"
        if alreadyRun: # Make function idempotent in case it double-fires
            logging.info(f'Task {task_id} has already been completed. Exiting COMBINE_SECTIONS.')
            {"task_id": task_id}

        final_jsonl_str = combine_JSONL(task_id, task_id_meta["section_tracker"], blob_connection_str_secret)
        final_file_id = task_id_meta["final_output_id"]
        upload_to_blob(final_jsonl_str, blob_connection_str_secret, "final-processed-results", final_file_id)
        download_filename = generate_valid_filename(task_id_meta["title"]) + ".jsonl"
        download_link = generate_blob_download_link(blob_connection_str_secret, "final-processed-results", final_file_id, download_filename)
        
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