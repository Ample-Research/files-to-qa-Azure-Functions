import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    RETRIEVE_RESULT is called by the front-end once processing is complete.
    It is triggered when CHECK_TASK_STATUS informs the front-end that the task is complete
    The front-end then sends an HTTP request to this function
    This function then performs two main tasks:
        1. Retrieves the download information for the final JSONL file based on the HTTP request
        2. Sends that download information to the front-end for the user to download
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
