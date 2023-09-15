import logging
import requests
import os

import azure.functions as func

from utils.create_error_msg import create_error_msg
from utils.init_function import init_function


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    DURABLE_FUNC_INTERACTIONS is a function that handle's inteactions with existing functions.
    It takes in the instance ID of the function and performs an action.
    For now, it will just check runtime status and/or terminate an orchestrator
    '''
    try:
        blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret = init_function("DURABLE_FUNC_INTERACTIONS", "HTTP")

        action = req.params.get('action')
        instance_id = req.params.get('instance_id') 

        function_master_code = os.environ.get('MASTER_HOST_KEY')
        staging_env = os.environ["StagingEnv"]
        if staging_env == 'PROD':
            function_url = "ample-files-to-qa"
            task_hub = "amplefilestoqaPRODUCTION"
        else:
            function_url = "ample-files-to-qa-development"
            task_hub = "amplefilestoqaDEVELOPMENT"

        base_url = f"https://{function_url}.azurewebsites.net/runtime/webhooks/durabletask/instances/{instance_id}"
        storage_conn = "AzureWebJobsStorage"

        if action == 'terminate':
            termination_reason = req.params.get('termination_reason')
            url = base_url + f"/terminate?taskHub={task_hub}&connection={storage_conn}&code={function_master_code}&reason={termination_reason}"
            method = 'POST'
        elif action == 'status':
            url = base_url + f"?taskHub={task_hub}&connection={storage_conn}&code={function_master_code}&showHistory=true"
            method = 'GET'
        else:
            return func.HttpResponse("Invalid action", status_code=400)
    
        response = requests.request(method, url)

        if response.status_code != 200:
            logging.error(f"Error performing {action} action on instance {instance_id}: {response.text}")
            return func.HttpResponse(response.text, status_code=response.status_code)
        
    except Exception as e:
        return create_error_msg(e, note="Error accessing Durbable Func in DURABLE_FUNC_INTERACTIONS")
    
    return func.HttpResponse(response.text, mimetype="application/json")