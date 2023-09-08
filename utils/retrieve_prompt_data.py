import os
import pandas as pd
import io
import logging

from utils.read_from_blob import read_from_blob


prompt_list_by_type = {
    "QA": ["question_extraction", "answer_extraction", "topic_tags_extraction"],
    "CHAT": []
}

def retrieve_prompt_data(task_type, blob_connection_str_secret):
    '''
    This function will take in a list of prompt names and retrieve 
    the corresponding prompt data from an Azure blob.
    '''
    if os.getenv('StagingEnv') != 'PROD':
        containter_name = "prompt-schematics-dev"
    else:
        containter_name = "prompt-schematics-prod"

    prompt_list = prompt_list_by_type[task_type]
    if len(prompt_list) == 0:
        logging.error(f"Invalid task_type: {task_type}")
        raise ValueError(f"Invalid task_type: {task_type}")

    all_prompt_data = []
    for prompt_name in prompt_list:
        this_prompt_csv_data = read_from_blob(blob_connection_str_secret, containter_name, f"{prompt_name}.csv")
        df = pd.read_csv(io.StringIO(this_prompt_csv_data.decode('utf-8')))
        this_prompt_data =  {
            "prompt": df["prompt"].iloc[0],
            "inputs": df["inputs"].iloc[0]
        }
        all_prompt_data.append(this_prompt_data)

    return tuple(all_prompt_data)