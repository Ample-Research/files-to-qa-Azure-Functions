import logging

import azure.functions as func


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
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
