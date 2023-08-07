import logging

import azure.functions as func


def main(msg: func.QueueMessage) -> None:
    '''
    SPLIT_INTO_SECTIONS enables faster processing for larger files.
    It is triggered by a Queue updated by CONVERT_TO_JSON.
    The Queue message will contain a JSON_File_ID and a Task_ID.
    This function performs four main tasks:
        1. Splits the JSON file (JSON_File_ID) into smaller sections
        2. Stores each of these sections in a blob under a File_ID_Section_ID
        3. Fans-Out these sections by triggering SECTION_ORCHESTRATOR, a durable function (More Research Required on this...)
        4. Updates Task_ID_Status (Task_ID) to mark section creation as complete & save section metadata (e.g. how many sections)
    '''
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
