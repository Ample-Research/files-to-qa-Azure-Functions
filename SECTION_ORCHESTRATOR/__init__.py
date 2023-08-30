# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.durable_functions as df

from utils.upload_to_blob import upload_to_blob
from utils.read_from_blob import read_from_blob
from utils.update_task_id_meta import update_task_id_metadata
from utils.retrieve_prompt_data import retrieve_prompt_data
from utils.init_function import init_function
from utils.split_into_section_batches import split_into_section_batches
from utils.process_section_batch import process_section_batch

def orchestrator_function(context: df.DurableOrchestrationContext):
    '''
    SECTION_ORCHESTRATOR is a durable function that manages the processing of all file sections.
    It is triggered by SPLIT_INTO_SECTIONS.

    More Research Required To Define These Specs... But generally:
        1. It triggers PROCESS_SECTION for every section
        2. It uses a Queue to trigger COMBINE_SECTIONS once all sections have been processed
    '''    
    
    try:
        start_time, blob_connection_str_secret, queue_connection_str_secret, error_msg = init_function("SECTION_ORCHESTRATOR", "ORCHESTRATOR")

        task_id_data_input = context.get_input()
        task_id = task_id_data_input["task_id"]
        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))
        task_type = task_id_meta["task_type"]
        
        prompt_data = retrieve_prompt_data(task_type, blob_connection_str_secret) # Differs for each task_type
        section_batches = split_into_section_batches(task_id_meta)
        for batch in section_batches:
            parallel_tasks = process_section_batch(batch, context, prompt_data, task_id)
            batch_results = yield context.task_all(parallel_tasks)
            if batch_results is not None: 
                for completed_task in batch_results:
                    updates = completed_task # PROCESS_SECTION will return updates
                    update_task_id_metadata(task_id_meta, updates, blob_connection_str_secret)

        updates = {
            "status": "sections_processed"
        }
        update_task_id_metadata(task_id_meta, updates, blob_connection_str_secret) 

        combine_sections_task = yield context.call_activity("COMBINE_SECTIONS", {"task_id": task_id})

        return f"SECTION_ORCHESTRATOR Returned for {task_id}"

    except Exception as e:
        logging.error(f"Exeption raised in SECTION_ORCHESTRATOR for task {task_id}: {str(e)}")
        task_id_meta["error_message"] = str(e)
        upload_to_blob(json.dumps(task_id_meta), blob_connection_str_secret, "tasks-meta-data", task_id)
        raise e

main = df.Orchestrator.create(orchestrator_function)