import logging
import json

from utils.fetch_credentials import fetch_credentials
from utils.upload_to_blob import upload_to_blob
from utils.read_from_blob import read_from_blob

from utils.extract_questions import extract_questions
from utils.extract_answers import extract_answers
from utils.extract_topic_tags import extract_topic_tags
from utils.create_QA_JSONL_str import create_QA_JSONL_str
from utils.retrieve_prompt_data import retrieve_prompt_data


def main(inputData: dict) -> dict:
    '''
    PROCESS_SECTION is the core processor that make the OpenAI API calls.
    It is triggered by the SECTION_ORCHESTRATOR, ideally processing each section in parallel.
    This function performs four main tasks:
        1. Uses OpenAI to process the section text into Question & Answer pairs, saved as JSONL
        2. Stores this JSONL output in a blob as something like File_ID_Section_ID_JSONL 
        3. Updates the SECTION_ORCHESTRATOR to mark File_ID_Section_ID as processed
        4. Updates Task_ID_Status (Task_ID) to mark this section processing as complete
    '''
    logging.info(f'PROCESS_SECTION function triggered!')

    section_id = inputData["section_id"]
    task_id = inputData["task_id"]

    try:
        blob_connection_str_secret, queue_connection_str_secret = fetch_credentials()
    except Exception as e:
        logging.error(f"Failed to connect credentials in PROCESS_SECTION for section {section_id}: {str(e)}")
        raise e
    
    try:
        
        task_id_meta_bytes = read_from_blob(blob_connection_str_secret, "tasks-meta-data", task_id)
        task_id_meta = json.loads(task_id_meta_bytes.decode('utf-8'))
        section_txt_bytes = read_from_blob(blob_connection_str_secret, "file-sections", section_id)
        section_txt = section_txt_bytes.decode('utf-8')

        prompt_names = ["question_extraction", "answer_extraction", "topic_tags_extraction"]
        question_prompt_data, answer_prompt_data, tags_prompt_data = retrieve_prompt_data(prompt_names, blob_connection_str_secret)

        section_questions = extract_questions(section_txt, task_id_meta, question_prompt_data, section_id)
        section_answers = extract_answers(section_txt, task_id_meta, section_questions, answer_prompt_data, section_id, blob_connection_str_secret)
        section_tags = extract_topic_tags(section_txt, task_id_meta, tags_prompt_data, section_id)

        section_QA_JSONL_str = create_QA_JSONL_str(section_questions, section_answers, task_id_meta, section_id)
        completed_section_id = section_id + "_jsonl"
        upload_to_blob(section_QA_JSONL_str, blob_connection_str_secret,"file-sections", completed_section_id)

        task_id_meta_updates = { # Updates to the metadata when the section completes
            "new_tags_list": section_tags,
            "section_id": section_id,
            "num_QA_pairs": len(section_questions)
        }

        return task_id_meta_updates

    except Exception as e:
        logging.error(f"Failed to process section in PROCESS_SECTION for section {section_id}: {str(e)}")
        raise e
