import logging
import json
import time

from utils.read_from_blob import read_from_blob
from utils.process_section_extract_QA import process_section_extract_QA
from utils.process_section_chat import process_section_chat
from utils.init_function import init_function

def main(inputData: dict) -> dict:
    '''
    Process section will process the text of a section given a task_type.
    Right now, we only have Q&A implemented, but we will add more.
    It calls the correct processing util, then makes the corresponding metadata updates.
    '''
    
    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = init_function("PROCESS_SECTION", "ACTION")

        section_id = inputData["section_id"]
        task_id = inputData["task_id"]
        prompt_data = inputData["prompt_data"]
        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))
        task_type = task_id_meta["task_type"]
        section_txt_bytes = read_from_blob(blob_connection_str_secret, "file-sections", section_id)
        section_txt = section_txt_bytes.decode('utf-8')

        if task_type == "QA":
            task_id_meta_updates = process_section_extract_QA(prompt_data, section_txt, task_id_meta, section_id, blob_connection_str_secret)
        elif task_type == "CHAT":
            task_id_meta_updates = process_section_chat()
        else: # Default to "QA"
            task_id_meta_updates = process_section_extract_QA(prompt_data, section_txt, task_id_meta, section_id, blob_connection_str_secret)

        logging.info(f"Section Task Completed In Orchestrator - Section ID: {section_id}")

        return task_id_meta_updates

    except Exception as e:
        logging.error(f"Failed to process section in PROCESS_SECTION for section {section_id}: {str(e)}")
        raise e
