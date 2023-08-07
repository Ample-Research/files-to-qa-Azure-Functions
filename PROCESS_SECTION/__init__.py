import logging

import azure.functions as func


def main(msg: func.QueueMessage) -> None:
    '''
    PROCESS_SECTION is the core processor that make the OpenAI API calls.
    It is triggered by a Queue updated with the SECTION_ORCHESTRATOR, ideally processing each section in parallel.
    This function performs four main tasks:
        1. Uses OpenAI to process the section text into Question & Answer pairs, saved as JSONL
        2. Stores this JSONL output in a blob as something like File_ID_Section_ID_JSONL 
        3. Updates the SECTION_ORCHESTRATOR to mark File_ID_Section_ID as processed
        4. Updates Task_ID_Status (Task_ID) to mark this section processing as complete
    '''
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
