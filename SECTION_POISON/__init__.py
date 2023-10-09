import logging
import json

import azure.functions as func

from utils.init_function import init_function
from utils.update_section_table import update_section_table

def main(msg: func.QueueMessage) -> None:
    '''
    1. Takes in poisoned section
    2. Sets its status to failed
    '''
    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = init_function("POISON_SECTION", "QUEUE")
        
        msg_data = json.loads(msg.get_body().decode('utf-8'))
        section_id = msg_data["section_id"]
        task_id = msg_data["task_id"]
        update_section_table(section_id, task_id, {"status": "failed"}, table_connection_str_secret)

    except Exception as e:
        logging.error(f"Failed to process poison section in POISON_SECTION for section {section_id}: {str(e)}... retrying")
        raise e