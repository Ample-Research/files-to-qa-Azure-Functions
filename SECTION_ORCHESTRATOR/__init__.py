# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    '''
    SECTION_ORCHESTRATOR is a durable function that manages the processing of all file sections.
    It is triggered by SPLIT_INTO_SECTIONS.

    More Research Required To Define These Specs... But generally:
        1. It triggers PROCESS_SECTION for every section
        2. It uses a Queue to trigger COMBINE_SECTIONS once all sections have been processed
    '''
    logging.info('SECTION_ORCHESTRATOR function triggered')

    result1 = yield context.call_activity('Hello', "Tokyo")
    result2 = yield context.call_activity('Hello', "Seattle")
    result3 = yield context.call_activity('Hello', "London")
    return [result1, result2, result3]

main = df.Orchestrator.create(orchestrator_function)