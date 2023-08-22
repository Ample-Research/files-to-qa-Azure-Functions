import logging
import requests
import os

import azure.functions as func

from utils.build_ping_req import build_ping_req

def main(mytimer: func.TimerRequest) -> None:
    if mytimer.past_due:
        logging.info('Running PING_INTERVAL...')

    if os.getenv('StagingEnv') == "DEV":
        return

    try:
        function_code = os.getenv('INIT_FUNC_CODE')
        init_url = f"https://ample-files-to-qa.azurewebsites.net/api/INITIATE_FILE_PROCESSING?code={function_code}"
        payload, files_payload = build_ping_req()
        response = requests.request("POST", init_url, data = payload, files = files_payload)

        if response.status_code == 200:
            response_data = response.json()
            task_id = response_data.get("task_id")
            logging.info(f'Successfully warmed up INITIATE_FILE_PROCESSING for task: {task_id}')
        else:
            logging.error('Failed to warm up INITIATE_FILE_PROCESSING')

    except Exception as e:
        logging.error(f'Error in PING_INTERVAL: {e}')

    logging.info('Python timer trigger function ran.')
