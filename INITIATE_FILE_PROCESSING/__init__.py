import logging
import json
import uuid

import azure.functions as func

from utils.init_task_data import init_task_data
from utils.create_error_msg import create_error_msg
from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.upload_to_queue import upload_to_queue

def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    INITIATE_FILE_PROCESSING is the entry point into this Q&A Processor. 
    The front-end sends a PDF, DOCX, TXT, or CSV file via an HTTP request.
    Then this function performs three main tasks:
        1. Creates a task instance, saving task_id_status into a blob to track the task progress
        2. Saves the raw uploaded file into an Azure Blob with a file_id
        3. Updates the Azure Queue with the File_ID and Task_ID to trigger CONVERT_TO_JSON
    Finally, this function returns the Task_ID back to the front-end.
    The front-end can use this idea to track progress with the CHECK_TASK_STATUS function
    '''
    logging.info('INITIATE_FILE_PROCESSING function hit')

    try:
        blob_connection_str_secret, queue_connection_str_secret = fetch_credentials()
    except Exception as e:
        return create_error_msg(e, note="Failed credentials in INITIATE_FILE_PROCESSING")
    
    try:

        config_data = json.loads(req.form['data']) if 'data' in req.form else None
        file_data = req.files['file'].read() if 'file' in req.files else None
        filename = req.files['file'].filename
        file_size_in_bytes = len(file_data) if file_data else 0
        
        if not file_data:
            raise ValueError("Missing file in the request in INITIATE_FILE_PROCESSING")
        if not config_data:
            raise ValueError("Missing config data in the request in INITIATE_FILE_PROCESSING")

        task_id = str(uuid.uuid4())
        task_id_meta = init_task_data(task_id, config_data, file_size_in_bytes, filename)
        file_id = task_id_meta["raw_file_id"]

        upload_to_blob(file_data, blob_connection_str_secret,"raw-file-uploads", file_id)
        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret,"tasks-meta-data", task_id)
        upload_to_queue(json.dumps(task_id_meta),queue_connection_str_secret, "convert-to-txt-queue")

        return func.HttpResponse(json.dumps(task_id_meta), mimetype="application/json") # Return task data to frontend
    
    except Exception as e:
        return create_error_msg(e, note="Error saving file in INITIATE_FILE_PROCESSING")