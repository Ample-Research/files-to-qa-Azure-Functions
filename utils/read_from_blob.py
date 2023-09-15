from azure.storage.blob import BlobClient
from utils.timeit import timeit

@timeit
def read_from_blob(blob_connection_str_secret, container_name, file_id):
    blob_client = BlobClient.from_connection_string(blob_connection_str_secret.value, container_name=container_name, blob_name=file_id)
    raw_file = blob_client.download_blob().readall()
    return raw_file