from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions, ContentSettings
from datetime import datetime, timedelta

def generate_blob_download_link(blob_connection_str_secret, container_name, blob_id, download_filename):
    blob_connection_str = blob_connection_str_secret.value
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_id)

    properties = blob_client.get_blob_properties()

    blob_headers = ContentSettings(content_disposition=f"attachment; filename={download_filename}",
                                   content_type=properties.content_settings.content_type,
                                   content_encoding=properties.content_settings.content_encoding,
                                   content_language=properties.content_settings.content_language,
                                   cache_control=properties.content_settings.cache_control,
                                   content_md5=properties.content_settings.content_md5)

    blob_client.set_http_headers(blob_headers)

    sas_token = generate_blob_sas(
          account_name=blob_service_client.account_name,
          container_name=container_name,
          blob_name=blob_id,
          account_key=blob_service_client.credential.account_key,
          permission=BlobSasPermissions(read=True),
          expiry=datetime.utcnow() + timedelta(weeks=1) # Expires in 1 week
      )

    return blob_client.url + "?" + sas_token