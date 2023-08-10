import logging
import json

from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.read_from_blob import read_from_blob

def main(inputData: dict) -> dict:
    '''
    COMBINE_SECTIONS will combined each section's JSONL into a single output file.
    It is triggered by SECTION_ORCHESTRATOR once each section is complete.
    This function performs three main tasks:
        1. Combines each section JSONL into a single large JSONL file
        2. Stores this final JSONL file inot a blob as the final result
        3. Updates Task_ID_Status (Task_ID) to mark processing as complete & gives it the Final File_ID
    '''
    logging.info(f'COMBINE_SECTIONS function triggered!')

    task_id = inputData["task_id"]

    try:
        blob_connection_str_secret, queue_connection_str_secret = fetch_credentials()
    except Exception as e:
        logging.error(f"Failed to connect credentials in COMBINE_SECTIONS for task {task_id}: {str(e)}")
        raise e

    try:
        
        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))

        return {"task_id": task_id}

    except Exception as e:
        logging.error(f"Failed to combine sections in COMBINE_SECTIONS for task {task_id}: {str(e)}")
        raise e