import logging
import json

import azure.functions as func
from azure.storage.blob import BlobServiceClient

from utils.create_error_msg import create_error_msg
from utils.read_from_table import read_from_table
from utils.init_function import init_function
from utils.check_sections_status import track_sections_completion

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

        task_id = req.params.get('task_id')
        if not task_id:
            raise ValueError("Missing task_id in the request in CHECK_TASK_STATUS")
        task_id_meta = read_from_table(task_id, "tasks", table_connection_str_secret)

        section_completion_percentage = 0
        if task_id_meta["status"] == "section_processing_triggered":
            section_completion_percentage = track_sections_completion(task_id, task_id_meta["num_sections"], table_connection_str_secret)

        task_id_meta["completion_percentage"] = section_completion_percentage
        
        return func.HttpResponse(json.dumps(task_id_meta), mimetype="application/json") # Return task meta-data to frontend

    except Exception as e:
        return create_error_msg(e, note=f"Error retrieving task status in CHECK_TASK_STATUS for task {task_id}")