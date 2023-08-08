from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def fetch_credentials():
      # Fetch secrets and credentials
    credential = DefaultAzureCredential()
    blob_connection_str_secret = SecretClient(vault_url="https://files-to-qa-keys.vault.azure.net/", credential=credential).get_secret("BLOB-CONNECTION-STRING")
    queue_connection_str_secret = SecretClient(vault_url="https://files-to-qa-keys.vault.azure.net/", credential=credential).get_secret("QUEUE-CONNECTION-STRING")
    return blob_connection_str_secret, queue_connection_str_secret