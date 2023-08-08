from azure.storage.blob import BlobClient

def upload_to_blob(file_data, blob_connection_str_secret, container_name, file_id):
    blob_client = BlobClient.from_connection_string(blob_connection_str_secret.value, container_name=container_name, blob_name=file_id)
    blob_client.upload_blob(file_data, overwrite=True)