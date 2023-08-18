import datetime

def init_runtime_metadata(task_id):
    '''
    Tracking the metadata for evaluating task efficiency.
    Stored in container: "qa-runtime-metadata"
    '''

    runtime_meta_data = {
        # Core Meta Data
        "task_id": task_id,
        "INITIATE_FILE_PROCESSING_timer": 0,
        "CONVERT_TO_TXT_timer": 0,
        "SPLIT_INTO_SECTIONS_timer": 0,
        "SECTION_ORCHESTRATOR_timer": 0,
        "COMBINE_SECTIONS_timer": 0,
        "PROCESS_SECTION_timer": {}, # Populate with section ids later
        "section_answer_tokens": {},
        "section_answer_choice": {},
        "section_question_gpt_timer": {},
        "section_answer_gpt_timer": {},
        "raw_gpt_answer_output" : {}
    }

    return runtime_meta_data
