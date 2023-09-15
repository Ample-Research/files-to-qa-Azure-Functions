from utils.extract_questions import extract_questions
from utils.extract_answers import extract_answers
from utils.extract_topic_tags import extract_topic_tags
from utils.create_QA_JSONL_str import create_QA_JSONL_str
from utils.upload_to_blob import upload_to_blob
from utils.timeit import timeit

@timeit
def process_section_extract_QA(prompt_data, section_txt, task_id_meta, section_id, blob_connection_str_secret):
    '''
    This used to be the PROCESS_SECTION before we started adding more user cases.
    It is now triggered by PROCESS_SECTION iff the task_type is set to QA.
    This function performs four main tasks:
        1. Uses OpenAI to process the section text into Question & Answer pairs, saved as JSONL
        2. Stores this JSONL output in a blob as something like File_ID_Section_ID_JSONL 
        3. Updates the SECTION_ORCHESTRATOR to mark File_ID_Section_ID as processed
        4. Updates Task_ID_Status (Task_ID) to mark this section processing as complete
    '''
    completed_section_id = section_id + "_jsonl"
    question_prompt_data, answer_prompt_data, tags_prompt_data = prompt_data

    section_questions = extract_questions(section_txt, task_id_meta, question_prompt_data, section_id)
    section_answers, answer_choice, answer_tokens = extract_answers(section_txt, task_id_meta, section_questions, answer_prompt_data, section_id, blob_connection_str_secret)
    section_tags = extract_topic_tags(section_txt, task_id_meta, tags_prompt_data, section_id)
    section_QA_JSONL_str = create_QA_JSONL_str(section_questions, section_answers, task_id_meta, section_id)
    num_QA_pairs = len(section_questions)

    return section_QA_JSONL_str, num_QA_pairs, section_tags, completed_section_id