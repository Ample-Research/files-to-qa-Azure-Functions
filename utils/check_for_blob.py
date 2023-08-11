from azure.storage.blob import BlobServiceClient

def check_for_blob(blob_connection_str_secret, container_name, file_id):
    blob_connection_str = blob_connection_str_secret.value
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_id)
    return blob_client.exists()
