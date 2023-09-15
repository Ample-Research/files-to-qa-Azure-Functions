import logging
import json

import azure.functions as func

from utils.extract_text_from_file import extract_text_from_file
from utils.read_from_blob import read_from_blob
from utils.init_function import init_function
from utils.split_into_sections import split_into_sections
from utils.trigger_sections import trigger_sections
from utils.update_task_id_meta import update_task_id_meta
from utils.retrieve_prompt_data import retrieve_prompt_data

def main(msg: func.QueueMessage) -> None:
    '''
    1. Takes in file id
    2. Converts the file to text
    3. Splits that text into sections
    4. Saves each section
    5. Adds each section_id to a queue
    '''
    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = init_function("PROCESS_FILE", "QUEUE")
       
        msg_data = json.loads(msg.get_body().decode('utf-8'))
        file_id = msg_data["file_id"]
        task_id = msg_data["task_id"]
        filename = msg_data["filename"]
        task_type = msg_data["task_type"]
        
        raw_file = read_from_blob(blob_connection_str_secret, "raw-file-uploads", file_id)
        txt_data = extract_text_from_file(raw_file, filename)
        sections = split_into_sections(txt_data)
        prompt_data = retrieve_prompt_data(task_type, blob_connection_str_secret)
        trigger_success = trigger_sections(sections, task_id, task_type, prompt_data, blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret)

        if trigger_success:
            update_task_id_meta(task_id, {"status": "section_processing_triggered"}, table_connection_str_secret)

    except Exception as e:
        logging.error(f"Failed PROCESS_FILE: {str(e)}")
        update_task_id_meta(task_id, {"error_message": str(e)})
        raise e