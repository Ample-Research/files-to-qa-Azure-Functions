import base64
import logging

from azure.storage.queue import QueueClient

def upload_to_queue(queue_message, queue_connection_str_secret, queue_name):
    queue_message_bytes = queue_message.encode('utf-8')
    queue_message_base64 = base64.b64encode(queue_message_bytes).decode('utf-8')
    queue_client = QueueClient.from_connection_string(queue_connection_str_secret.value, queue_name=queue_name)
    queue_client.send_message(queue_message_base64)