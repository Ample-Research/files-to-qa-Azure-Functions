import logging
import json
import uuid
import os
import time


import azure.functions as func

from utils.init_task_data import init_task_data
from utils.create_error_msg import create_error_msg
from utils.upload_to_blob import upload_to_blob
from utils.upload_to_queue import upload_to_queue
from utils.init_function import init_function

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
    
    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = init_function("INITIATE_FILE_PROCESSING", "HTTP")
        config_data = json.loads(req.form['data']) if 'data' in req.form else None
        file_data = req.files['file'].read() if 'file' in req.files else None
        filename = req.files['file'].filename
        file_size_in_bytes = len(file_data) if file_data else 0
        task_type = config_data.get("task_type", "QA")

        if not file_data:
            raise ValueError("Missing file in the request in INITIATE_FILE_PROCESSING")
        if not config_data:
            raise ValueError("Missing config data in the request in INITIATE_FILE_PROCESSING")

        task_id = init_task_data(config_data, file_size_in_bytes, filename, table_connection_str_secret)
        file_id = f"{task_id}_raw"

        upload_to_blob(file_data, blob_connection_str_secret,"raw-file-uploads", file_id)

        queue_msg = {
            "file_id": file_id,
            "task_id": task_id,
            "filename": filename,
            "task_type": task_type
        }

        upload_to_queue(json.dumps(queue_msg), queue_connection_str_secret, os.environ["PROCESS_FILE_QUEUE"])

        return func.HttpResponse(json.dumps({"task_id": task_id}), mimetype="application/json")
    
    except Exception as e:
        return create_error_msg(e, note="Error saving file in INITIATE_FILE_PROCESSING")
    


