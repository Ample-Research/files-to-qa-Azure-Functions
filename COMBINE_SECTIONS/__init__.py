import logging
import json

import azure.functions as func

from utils.update_task_id_meta import update_task_id_meta
from utils.init_function import init_function
from utils.combine_qa import combine_qa
from utils.combine_chat import combine_chat
from utils.update_task_id_meta import update_task_id_meta

def main(msg: func.QueueMessage) -> None:
    '''
    1. Takes in file id
    2. Converts the file to text
    3. Splits that text into sections
    4. Saves each section
    5. Adds each section_id to a queue
    '''
    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = init_function("COMBINE_SECTIONS", "QUEUE")
       
        msg_data = json.loads(msg.get_body().decode('utf-8'))
        task_id = msg_data["task_id"]
        num_sections = msg_data["total_num_sections"]
        task_type = msg_data["task_type"]
        title = msg_data["title"]
        
        if task_type == "QA":
            download_link = combine_qa(task_id, num_sections, title, blob_connection_str_secret, table_connection_str_secret)
        
        elif task_type == "CHAT":
            download_link = combine_chat() # NOT IMPLEMENTED
        
        update_task_id_meta(task_id, {"status": "complete", "download_link": download_link}, table_connection_str_secret)

    except Exception as e:
        logging.error(f"Failed PROCESS_FILE: {str(e)}")
        update_task_id_meta(task_id, {"error_message": str(e)}, table_connection_str_secret)
        raise e