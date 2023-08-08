import logging

import azure.functions as func

import logging
import json

import azure.functions as func

from utils.extract_text_from_file import extract_text_from_file
from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.upload_to_queue import upload_to_queue
from utils.read_from_blob import read_from_blob
from utils.fire_orchestrator import fire_orchestrator


def main(msg: func.QueueMessage, starter: str) -> None:
    '''
    SPLIT_INTO_SECTIONS enables faster processing for larger files.
    It is triggered by a Queue updated by CONVERT_TO_JSON.
    The Queue message will contain the Task_ID meta-data.
    This function performs four main tasks:
        1. Splits the TXT file into smaller sections
        2. Stores each of these sections in a blob under {task_id}_section_{section_number}
        3. Fans-Out these sections by triggering SECTION_ORCHESTRATOR
        4. Updates Task_ID_Status (Task_ID) to mark section creation as complete & save section metadata (e.g. how many sections)
    '''
    logging.info('SPLIT_INTO_SECTIONS function triggered')

    try:
        blob_connection_str_secret, queue_connection_str_secret = fetch_credentials()
    except Exception as e:
        logging.error(f"Failed to connect credentials in CONVERT_TO_TXT: {e}")
        raise e

    try:
        
        # # Code from CONVERT_TO_TXT
        # task_id_meta = json.loads(msg.get_body().decode('utf-8'))
        # file_id = task_id_meta["raw_file_id"]
        # task_id = task_id_meta["task_id"]
        # filename = task_id_meta["filename"]
        # raw_text_id = task_id_meta["raw_text_id"]

        # raw_file = read_from_blob(blob_connection_str_secret, "raw-file-uploads", file_id)
        # txt_data = extract_text_from_file(raw_file, filename)
        # upload_to_blob(txt_data, blob_connection_str_secret,"raw-text-files", raw_text_id)

        task_id_meta = json.loads(msg.get_body().decode('utf-8'))
        task_id = task_id_meta["task_id"]
        raw_text_id = task_id_meta["raw_text_id"] # Stored in blob: "raw-text-files"

        # PSUEDO-CODE

            # Split into sections

            # Save each section in its own blob as "{task_id}_section_{section_number}"
                # upload_to_blob(txt_data, blob_connection_str_secret,"file-sections", raw_text_id)

            # Populate task_id_meta["section_tracker"] with each section's ID & status

        task_id_meta["section_tracker"] = {} # You will need to populate this

        task_id_meta["status"] = "sections_processed"
        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret,"tasks-meta-data", task_id)
        instance_id = fire_orchestrator(starter, "SECTION_ORCHESTRATOR", task_id_meta["section_tracker"])
        
        logging.info(f"Started orchestration with ID = '{instance_id}'")

    except Exception as e:
        logging.error(f"Failed to split & save sections in SPLIT_INTO_SECTIONS: {e}")
        raise e