# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df

from utils.extract_text_from_file import extract_text_from_file
from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.upload_to_queue import upload_to_queue
from utils.read_from_blob import read_from_blob
from utils.upload_task_error import upload_task_error

def orchestrator_function(context: df.DurableOrchestrationContext):
    '''
    SECTION_ORCHESTRATOR is a durable function that manages the processing of all file sections.
    It is triggered by SPLIT_INTO_SECTIONS.

    More Research Required To Define These Specs... But generally:
        1. It triggers PROCESS_SECTION for every section
        2. It uses a Queue to trigger COMBINE_SECTIONS once all sections have been processed
    '''
    task_id_data_input = context.get_input()
    task_id = task_id_data_input["task_id"]
    logging.info(f'SECTION_ORCHESTRATOR function triggered for task: {task_id}')
    
    try:
        blob_connection_str_secret, queue_connection_str_secret = fetch_credentials()
    except Exception as e:
        logging.error(f"Failed to connect credentials in SECTION_ORCHESTRATOR: {str(e)}")
        raise e
    
    try:

        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))
        section_tracker = task_id_meta["section_tracker"]

        parallel_tasks = [context.call_activity("PROCESS_SECTION", {"section_id": section_id, "task_id": task_id})
                         for section_id, status in section_tracker.items() if status != "completed"]

        yield context.task_all(parallel_tasks)

        for completed_task in parallel_tasks:
            result = completed_task.result
            logging.info(f"Section Task Completed In Orchestrator - Section ID: {result['section_id']}")
            task_id_meta["section_tracker"][result["section_id"]] = "completed"
            task_id_meta["tags"] = list(set(task_id_meta["tags"] + result["new_tags_list"]))
            task_id_meta["num_QA_pairs"] += result["num_QA_pairs"]

        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret, "tasks-meta-data", task_id)
        
        combine_sections_task = yield context.call_activity("COMBINE_SECTIONS", {"task_id": task_id})

    except Exception as e:
        logging.error(f"Exeption raised in SECTION_ORCHESTRATOR for task {task_id}: {str(e)}")
        raise e

    return f"SECTION_ORCHESTRATOR Returned for {task_id}"

main = df.Orchestrator.create(orchestrator_function)