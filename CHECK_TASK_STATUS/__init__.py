import logging
import json

import azure.functions as func
from azure.storage.blob import BlobServiceClient

from utils.create_error_msg import create_error_msg
from utils.fetch_credentials import fetch_credentials
from utils.read_from_blob import read_from_blob

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
    logging.info('CHECK_TASK_STATUS function hit')

    try:
        blob_connection_str_secret, queue_connection_str_secret = fetch_credentials()
    except Exception as e:
        return create_error_msg(e, note="Failed credentials in INITIATE_FILE_PROCESSING")

    try:
        task_id = req.params.get('task_id')
        if not task_id:
            raise ValueError("Missing task_id in the request in CHECK_TASK_STATUS")
        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))

        blob_connection_str = blob_connection_str_secret.value
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_str)
        section_ids = task_id_meta["section_tracker"]
        for section_id in section_ids.keys(): # Look at each section id and determine if a _jsonl file exists in blob
            jsonl_id = section_id + "_jsonl"
            blob_client = blob_service_client.get_blob_client(container="file-sections", blob=jsonl_id)
            if blob_client.exists():
                task_id_meta["section_tracker"][section_id] = "completed"

        return func.HttpResponse(json.dumps(task_id_meta), mimetype="application/json") # Return task meta-data to frontend

    except Exception as e:
        return create_error_msg(e, note=f"Error retrieving task status in CHECK_TASK_STATUS for task {task_id}")