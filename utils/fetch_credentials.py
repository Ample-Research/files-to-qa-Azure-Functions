import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableClient
vault_url = os.environ["VAULT_URL"]
from utils.timeit import timeit

@timeit
def fetch_credentials():
      # Fetch secrets and credentials
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=vault_url, credential=credential)

    blob_connection_str_secret = secret_client.get_secret("BLOB-CONNECTION-STRING")
    queue_connection_str_secret = secret_client.get_secret("QUEUE-CONNECTION-STRING")
    table_connection_str_secret = secret_client.get_secret("TABLE-CONNECTION-STRING")

    return blob_connection_str_secret, queue_connection_str_secret, table_connection_str_secret