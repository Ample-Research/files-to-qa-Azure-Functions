import logging

import azure.functions as func


def main(msg: func.QueueMessage) -> None:
    '''
    COMBINE_SECTIONS will combined each section's JSONL into a single output file.
    It is triggered by a Queue updated by SECTION_ORCHESTRATOR once each section is complete.
    The Queue message will contain all of the section IDs (File_ID_Section_ID)
    This function performs three main tasks:
        1. Combines each section JSONL into a single large JSONL file
        2. Stores this final JSONL file inot a blob as the final result
        3. Updates Task_ID_Status (Task_ID) to mark processing as complete & gives it the Final File_ID
    '''
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
