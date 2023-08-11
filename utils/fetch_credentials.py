import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
vault_url = os.environ["VAULT_URL"]

def fetch_credentials():
      # Fetch secrets and credentials
    credential = DefaultAzureCredential()
    blob_connection_str_secret = SecretClient(vault_url=vault_url, credential=credential).get_secret("BLOB-CONNECTION-STRING")
    queue_connection_str_secret = SecretClient(vault_url=vault_url, credential=credential).get_secret("QUEUE-CONNECTION-STRING")
    return blob_connection_str_secret, queue_connection_str_secret