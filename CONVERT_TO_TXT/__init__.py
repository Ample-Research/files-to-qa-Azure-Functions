import logging
import json

import azure.functions as func

from azure.storage.blob import BlobClient
from azure.storage.queue import QueueClient
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from utils.extract_text_from_file import extract_text_from_file

def main(msg: func.QueueMessage) -> None:
    '''
    CONVERT_TO_TXT is the first processing step.
    It is triggered by a Queue updated by INITIATE_FILE_PROCESSING.
    The Queue message will contain a File_ID and a Task_ID.
    This function performs four main tasks:
        1. Processes the raw file (File_ID) into a JSON format
        2. Stores this JSON in a blob under a JSON_File_ID
        3. Updates the Azure Queue with this JSON_File_ID to trigger SPLIT_INTO_SECTIONS
        4. Updates Task_ID_Status (Task_ID) to mark JSON processing as complete
    '''
    logging.info('CONVERT_TO_TXT function triggered')

    try:

        # Fetch secrets and credentials
        credential = DefaultAzureCredential()
        blob_connection_str_secret = SecretClient(vault_url="https://files-to-qa-keys.vault.azure.net/", credential=credential).get_secret("BLOB-CONNECTION-STRING")
        queue_connection_str_secret = SecretClient(vault_url="https://files-to-qa-keys.vault.azure.net/", credential=credential).get_secret("QUEUE-CONNECTION-STRING")

    except Exception as e:
        logging.error(f"Error during CONVERT_TO_JSON while getting Azure Credentials: {str(e)}")
    
        error_response = {
            "status": "error",
            "message": f"Failed to process the request. Error: {str(e)}"
        }

        return func.HttpResponse(json.dumps(error_response), status_code=500, mimetype="application/json")

    try:

        # Extract message from queue
        task_data = json.loads(msg.get_body().decode('utf-8'))
        file_id = task_data["raw_file_id"]
        task_id = task_data["task_id"]
        filename = task_data["filename"]

    except Exception as e:
        logging.error(f"Error during CONVERT_TO_JSON while reading queue message data: {str(e)}")
    
        error_response = {
            "status": "error",
            "message": f"Failed to process the request. Error: {str(e)}"
        }

    try:

        blob_client = BlobClient.from_connection_string(blob_connection_str_secret.value, container_name="raw-file-uploads", blob_name=file_id)
        raw_file = blob_client.download_blob().readall()
        json_data = extract_text_from_file(raw_file, filename)

    except Exception as e:
        logging.error(f"Error during CONVERT_TO_JSON while converting file: {str(e)}")
    
        error_response = {
            "status": "error",
            "message": f"Failed to process the request. Error: {str(e)}"
        }

    # Save to blob, update task status, trigger next function w/ queue


    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
