import time
import json

from utils.read_from_blob import read_from_blob
from utils.upload_to_blob import upload_to_blob
from utils.init_runtime_metadata import init_runtime_metadata

def update_runtime_metadata(start_time, function_name, task_id, blob_connection_str_secret, section_tracker = {}, 
                            section_id = "", q_execution_time = 0, a_execution_time = 0, answer_choice = 0,
                            answer_tokens = 0):
    '''
    Updates relevant metadata from various functions for custom performance tracking
    '''
  
    runtime_metadata_id = task_id + "_runtime"
    end_time = time.time()
    execution_time = end_time - start_time

    if function_name == "INITIATE_FILE_PROCESSING":
        runtime_metadata = init_runtime_metadata(task_id)
    else:
        runtime_metadata = read_from_blob(blob_connection_str_secret, "qa-runtime-metadata", runtime_metadata_id)

    if function_name == "SPLIT_INTO_SECTIONS":
        runtime_metadata["PROCESS_SECTION_timer"] = section_tracker
        runtime_metadata["section_answer_tokens"] = section_tracker
        runtime_metadata["section_answer_choice"] = section_tracker
        runtime_metadata["section_question_gpt_timer"] = section_tracker
        runtime_metadata["section_answer_gpt_timer"] = section_tracker

    if function_name == "PROCESS_SECTION":
        runtime_metadata["PROCESS_SECTION_timer"][section_id] = execution_time
        runtime_metadata["section_answer_tokens"][section_id] = answer_tokens
        runtime_metadata["section_answer_choice"][section_id] = answer_choice
        runtime_metadata["section_question_gpt_timer"][section_id] = q_execution_time
        runtime_metadata["section_answer_gpt_timer"][section_id] = a_execution_time
        upload_to_blob(json.dumps(runtime_metadata), blob_connection_str_secret,"qa-runtime-metadata", runtime_metadata_id)
        return

    runtime_metadata[function_name + "_timer"] = execution_time
    upload_to_blob(json.dumps(runtime_metadata), blob_connection_str_secret, "qa-runtime-metadata", runtime_metadata_id)
    
    return