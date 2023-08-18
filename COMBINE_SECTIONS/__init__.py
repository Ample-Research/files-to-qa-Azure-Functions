import logging
import json
import time

from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.read_from_blob import read_from_blob
from utils.update_runtime_metadata import update_runtime_metadata
from utils.generate_blob_download_link import generate_blob_download_link
from utils.generate_valid_filename import generate_valid_filename
from utils.validate_jsonl_format import validate_jsonl_format

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
    logging.info(f'COMBINE_SECTIONS function triggered!')
    start_time = time.time()
    task_id = inputData["task_id"]

    try:
        blob_connection_str_secret, queue_connection_str_secret = fetch_credentials()
    except Exception as e:
        logging.error(f"Failed to connect credentials in COMBINE_SECTIONS for task {task_id}: {str(e)}")
        raise e

    try:
        
        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))

        alreadyRun = task_id_meta["status"] == "completed"
        if alreadyRun: # Make function idempotent in case it double-fires
            logging.info(f'Task {task_id} has already been completed. Exiting COMBINE_SECTIONS.')
            {"task_id": task_id}

        section_ids = task_id_meta["section_tracker"]
        completed_section_ids = [key + "_jsonl" for key, value in section_ids.items() if value == "completed"]

        combined_jsonl = ""
        for jsonl_section_id in completed_section_ids:
            section_content_bytes = read_from_blob(blob_connection_str_secret, "file-sections", jsonl_section_id)
            combined_jsonl += section_content_bytes.decode('utf-8') + "\n"
        final_jsonl_str = validate_jsonl_format(combined_jsonl, task_id)

        final_file_id = task_id_meta["final_output_id"]
        upload_to_blob(final_jsonl_str, blob_connection_str_secret, "final-processed-results", final_file_id)

        download_filename = generate_valid_filename(task_id_meta["title"]) + ".jsonl"
        download_link = generate_blob_download_link(blob_connection_str_secret, "final-processed-results", final_file_id, download_filename)
        task_id_meta["download_link"] = download_link
        task_id_meta["status"] = "completed"
        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret, "tasks-meta-data", task_id)

        logging.info(f'COMBINE_SECTIONS function for task {task_id} successfully completed!')
        
        update_runtime_metadata(start_time, "COMBINE_SECTIONS", task_id, blob_connection_str_secret)

        return {"task_id": task_id}

    except Exception as e:
        logging.error(f"Failed to combine sections in COMBINE_SECTIONS for task {task_id}: {str(e)}")
        task_id_meta["error_message"] = str(e)
        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret, "tasks-meta-data", task_id)
        raise e