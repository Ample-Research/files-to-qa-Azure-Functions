import logging
import json
import os

import azure.functions as func

from utils.read_from_blob import read_from_blob
from utils.process_section_extract_QA import process_section_extract_QA
from utils.process_section_chat import process_section_chat
from utils.init_function import init_function
from utils.upload_to_blob import upload_to_blob
from utils.update_section_table import update_section_table
from utils.update_task_id_meta import increment_numerical_field, append_tag_field
from utils.read_from_table import read_from_table
from utils.check_sections_status import check_sections_status
from utils.upload_to_queue import upload_to_queue
from utils.update_task_id_meta import update_task_id_meta


def main(msg: func.QueueMessage) -> None:
    '''
    1. Takes in section id
    2. Retrieves the section
    3. Processes the section
    4. Updates Section Table
    5. Re-runs if there is an error
    '''
    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = init_function("PROCESS_SECTION", "ACTION")
        
        msg_data = json.loads(msg.get_body().decode('utf-8'))
        section_id = msg_data["section_id"]
        task_id = msg_data["task_id"]
        prompt_data = msg_data["prompt_data"]
        task_type = msg_data["task_type"]

        section_txt_bytes = read_from_blob(blob_connection_str_secret, "file-sections", section_id)
        section_txt = section_txt_bytes.decode('utf-8')
        task_id_meta = read_from_table(task_id, "tasks", "tasks", table_connection_str_secret)
        total_num_sections = task_id_meta["num_sections"]
        title = task_id_meta["title"]
        
        if task_type == "QA":
            section_QA_JSONL_str, num_QA_pairs, section_tags, completed_section_id = process_section_extract_QA(prompt_data, section_txt, task_id_meta, section_id, blob_connection_str_secret)

            if section_QA_JSONL_str and num_QA_pairs:
                upload_to_blob(section_QA_JSONL_str, blob_connection_str_secret,"file-sections-output", completed_section_id)
                increment_numerical_field(task_id, "num_QA_pairs",  num_QA_pairs, table_connection_str_secret)
                append_tag_field(task_id, section_tags, table_connection_str_secret)
                update_section_table(section_id, task_id, {"status": "complete"}, table_connection_str_secret)
            else: # Failed
                update_section_table(section_id, task_id, {"status": "failed"}, table_connection_str_secret)

        elif task_type == "CHAT":
            chat_info = process_section_chat() # NOT IMPLEMENTED

        # Check if all sections for task are complete
        all_sections_complete = check_sections_status(task_id, total_num_sections, table_connection_str_secret)
        if all_sections_complete: # Or failed
            queue_msg = {
                "task_id": task_id,
                "total_num_sections": total_num_sections,
                "task_type": task_type,
                "title": title
            }
            upload_to_queue(json.dumps(queue_msg), queue_connection_str_secret, os.environ["COMBINE_SECTIONS_QUEUE"])
            update_task_id_meta(task_id, {"status": "sections_processed"}, table_connection_str_secret)

    except Exception as e:
        logging.error(f"Failed to process section in PROCESS_SECTION for section {section_id}: {str(e)}... retrying")
        raise e
    
        # # RETRY IF FAILED —— TBD
        # section_meta = read_from_table(section_id, task_id, "sections", table_connection_str_secret)
        # if section_meta["status"] == "initiated":
        #     update_section_table(section_id, task_id, {"status": "retrying"}, table_connection_str_secret)
            
        #     queue_msg = {
        #     "section_id": section_id, 
        #     "task_id": task_id, 
        #     "prompt_data": prompt_data, 
        #     "task_type": task_type
        #     }
        #     upload_to_queue(json.dumps(queue_msg), queue_connection_str_secret, os.environ["PROCESS_SECTION_QUEUE"])