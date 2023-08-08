from azure.storage.queue import QueueClient

def upload_to_queue(queue_message, queue_connection_str_secret, queue_name):
    queue_client = QueueClient.from_connection_string(queue_connection_str_secret.value, queue_name=queue_name)
    queue_client.send_message(queue_message)