import logging
import json

import azure.functions as func

from utils.extract_text_from_file import extract_text_from_file
from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.upload_to_queue import upload_to_queue
from utils.read_from_blob import read_from_blob

def main(msg: func.QueueMessage) -> None:
    '''
    CONVERT_TO_TXT is the first processing step.
    It is triggered by a Queue updated by INITIATE_FILE_PROCESSING.
    The Queue message will contain a File_ID and a Task_ID.
    This function performs four main tasks:
        1. Processes the raw file (File_ID) into a TXT format
        2. Stores this JSON in a blob under a TXT_File_ID
        3. Updates the Azure Queue with this TXT_File_ID to trigger SPLIT_INTO_SECTIONS
        4. Updates Task_ID_Status (Task_ID) to mark JSON processing as complete
    '''
    logging.info('CONVERT_TO_TXT function triggered')

    try:
        blob_connection_str_secret, queue_connection_str_secret = fetch_credentials()
    except Exception as e:
        logging.error(f"Failed to connect credentials in CONVERT_TO_TXT: {e}")
        raise e

    try:
        task_id_meta = json.loads(msg.get_body().decode('utf-8'))
        file_id = task_id_meta["raw_file_id"]
        task_id = task_id_meta["task_id"]
        filename = task_id_meta["filename"]
        raw_text_id = task_id_meta["raw_text_id"]

        raw_file = read_from_blob(blob_connection_str_secret, "raw-file-uploads", file_id)
        txt_data = extract_text_from_file(raw_file, filename)
        upload_to_blob(txt_data, blob_connection_str_secret,"raw-text-files", raw_text_id)
        task_id_meta["status"] = "txt_processed"
        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret,"tasks-meta-data", task_id)
        upload_to_queue(json.dumps(task_id_meta),queue_connection_str_secret, "split-sections-queue")

    except Exception as e:
        logging.error(f"Failed to convert to txt in CONVERT_TO_TXT: {e}")
        raise e