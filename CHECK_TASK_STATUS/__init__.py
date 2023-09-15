import logging
import json

import azure.functions as func
from azure.storage.blob import BlobServiceClient

from utils.create_error_msg import create_error_msg
from utils.fetch_credentials import fetch_credentials
from utils.read_from_blob import read_from_blob
from utils.check_for_blob import check_for_blob
from utils.init_function import init_function

def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    CHECK_TASK_STATUS is called at intervals from the front-end to check the task status. 
    The front-end sends a task_id via an HTTP request.
    Then this function then performs three main tasks:
        1. Uses the task_id to check the status of the task by extracing task_id_status JSON from a blob
        2. Returns that task_id_status JSON to the front-end
    Note, the front-end will handle how to actually deal with this JSON data.
    For example, when the task is complete, the front-end must know to stop sending requests based on the JSON.
    '''

    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = init_function("CHECK_TASK_STATUS", "HTTP")
        if error_msg:
            return error_msg

        task_id = req.params.get('task_id')
        if not task_id:
            raise ValueError("Missing task_id in the request in CHECK_TASK_STATUS")
        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))

        # # Commented out becasue it is drastically slowing down the performance. Not work it.
        # section_ids = task_id_meta["section_tracker"]
        # for section_id in section_ids.keys(): # Determine if a _jsonl file exists
        #         jsonl_id = section_id + "_jsonl"
        #         isExists = check_for_blob(blob_connection_str_secret, "file-sections-output", jsonl_id)
        #         if isExists:
        #             task_id_meta["section_tracker"][section_id] = "completed"

        return func.HttpResponse(json.dumps(task_id_meta), mimetype="application/json") # Return task meta-data to frontend

    except Exception as e:
        return create_error_msg(e, note=f"Error retrieving task status in CHECK_TASK_STATUS for task {task_id}")