import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    INITIATE_FILE_PROCESSING is the entry point into this Q&A Processor. 
    The front-end sends a PDF, DOCX, TXT, or CSV file via an HTTP request.
    Then this function performs three main tasks:
        1. Creates a task instance, saving task_id_status into a blob to track the task progress
        2. Saves the raw uploaded file into an Azure Blob with a file_id
        3. Updates the Azure Queue with the File_ID and Task_ID to trigger CONVERT_TO_JSON
    Finally, this function returns the Task_ID back to the front-end.
    The front-end can use this idea to track progress with the CHECK_TASK_STATUS function
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
