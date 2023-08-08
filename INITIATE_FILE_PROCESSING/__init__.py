import logging
import json
import uuid

import azure.functions as func

from azure.storage.blob import BlobClient
from azure.storage.queue import QueueClient
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from utils.init_task_data import init_task_data


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
    logging.info('INITIATE_FILE_PROCESSING function hit')

    try:

        # Fetch secrets and credentials
        credential = DefaultAzureCredential()
        blob_connection_str_secret = SecretClient(vault_url="https://files-to-qa-keys.vault.azure.net/", credential=credential).get_secret("BLOB-CONNECTION-STRING")
        queue_connection_str_secret = SecretClient(vault_url="https://files-to-qa-keys.vault.azure.net/", credential=credential).get_secret("QUEUE-CONNECTION-STRING")

    except Exception as e:
        logging.error(f"Error during INITIATE_FILE_PROCESSING while getting Azure Credentials: {str(e)}")
    
        error_response = {
            "status": "error",
            "message": f"Failed to process the request. Error: {str(e)}"
        }

        return func.HttpResponse(json.dumps(error_response), status_code=500, mimetype="application/json")
    
    try:
        logging.info(f"Received data: {req.form['data']}")

        config_data = json.loads(req.form['data']) if 'data' in req.form else None


        # Get data from request
        file_data = req.files['file'].read() if 'file' in req.files else None
        filename = req.files['file'].filename
        file_size_in_bytes = len(file_data) if file_data else 0
        
        if not file_data:
            return func.HttpResponse(json.dumps({"status": "error", "message": "Missing file in the request"}), status_code=400, mimetype="application/json")

        if not config_data:
            return func.HttpResponse(json.dumps({"status": "error", "message": "Missing metadata in the request"}), status_code=400, mimetype="application/json")

    except Exception as e:
        logging.error(f"Error during INITIATE_FILE_PROCESSING while getting reading file & config data: {str(e)}")
    
        error_response = {
            "status": "error",
            "message": f"Failed to process the request. Error: {str(e)}"
        }

        return func.HttpResponse(json.dumps(error_response), status_code=500, mimetype="application/json")

    try:
        # Create the unique IDs
        task_id = str(uuid.uuid4())
        task_id_meta = init_task_data(task_id, config_data, file_size_in_bytes, filename)
        file_id = task_id_meta["raw_file_id"]

        # Save the raw uploaded file to Blob storage
        blob_client = BlobClient.from_connection_string(blob_connection_str_secret.value, container_name="raw-file-uploads", blob_name=file_id)
        blob_client.upload_blob(file_data, overwrite=True)

        # Create an empty task and store its status to Blob storage
        task_status_blob_client = BlobClient.from_connection_string(blob_connection_str_secret.value, container_name="tasks-meta-data", blob_name=task_id)
        task_status_blob_client.upload_blob(json.dumps(task_id_meta), overwrite=True)

        # Add message to Queue to trigger next function
        queue_client = QueueClient.from_connection_string(queue_connection_str_secret.value, queue_name="convert-to-txt-queue")
        queue_message = task_id_meta
        queue_client.send_message(json.dumps(queue_message))

        # Return task  data to frontend
        return func.HttpResponse(json.dumps(task_id_meta), mimetype="application/json")
    
    # Add more granular exception handling (e.g., specific errors for blob storage failures, queue failures, etc.)
    except Exception as e:
        logging.error(f"Error during INITIATE_FILE_PROCESSING: {str(e)}")
    
        error_response = {
            "status": "error",
            "message": f"Failed to process the request. Error: {str(e)}",
        }

        return func.HttpResponse(json.dumps(error_response), status_code=500, mimetype="application/json")

