import logging

import azure.functions as func


def main(msg: func.QueueMessage) -> None:
    '''
    CONVERT_TO_JSON is the first processing step.
    It is triggered by a Queue updated by INITIATE_FILE_PROCESSING.
    The Queue message will contain a File_ID and a Task_ID.
    This function performs four main tasks:
        1. Processes the raw file (File_ID) into a JSON format
        2. Stores this JSON in a blob under a JSON_File_ID
        3. Updates the Azure Queue with this JSON_File_ID to trigger SPLIT_INTO_SECTIONS
        4. Updates Task_ID_Status (Task_ID) to mark JSON processing as complete
    '''
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
