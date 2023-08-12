import logging

import azure.functions as func

import logging
import json

import azure.functions as func

from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.read_from_blob import read_from_blob
from utils.fire_orchestrator import fire_orchestrator
from utils.split_into_sections import split_into_sections


async def main(msg: func.QueueMessage, starter: str) -> None:
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
        logging.error(f"Failed to connect credentials in SPLIT_INTO_SECTIONS: {str(e)}")
        raise e

    try:
        
        task_id_meta = json.loads(msg.get_body().decode('utf-8'))
        task_id = task_id_meta["task_id"]
        raw_text_id = task_id_meta["raw_text_id"] # Stored in blob: "raw-text-files"
        raw_txt_bytes = read_from_blob(blob_connection_str_secret, "raw-text-files", raw_text_id)
        raw_txt = raw_txt_bytes.decode('utf-8')

        sections = split_into_sections(raw_txt)
        section_tracker = {}
        for idx, section in enumerate(sections):
            this_section_id = f"{task_id}_section_{str(idx)}"
            upload_to_blob(section, blob_connection_str_secret,"file-sections", this_section_id)
            section_tracker[this_section_id] = "initiated"

        task_id_meta["section_tracker"] = section_tracker # To track section IDs and status
        task_id_meta["status"] = "sections_created"

        instance_id = await fire_orchestrator(starter, "SECTION_ORCHESTRATOR", task_id_meta)
        logging.info(f"Started orchestration with ID = '{instance_id}'")
        task_id_meta["orchestrator_id"] = instance_id

        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret,"tasks-meta-data", task_id)

    except Exception as e:
        logging.error(f"Failed to split & save sections in SPLIT_INTO_SECTIONS: {str(e)}")
        task_id_meta["error_message"] = str(e)
        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret,"tasks-meta-data", task_id)
        raise e