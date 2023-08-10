import re
import json
import logging

from utils.build_prompt import build_prompt
from utils.query_openai import query_openai_chat
from utils.upload_to_blob import upload_to_blob


def extract_answers(section_txt, task_id_meta, questions, prompt_data, section_id, blob_connection_str_secret):
    '''
    This function will take in an blockof txt and a list of questions related to that txt.
    It will then use OpenAI to generate robust answers to those questions using the article.
    It will utilize the prompts stored in `answer_extraction.csv`
    '''

    model_name = task_id_meta["model_name"]
    if model_name == "gpt-3.5-turbo":
      model_name = "gpt-3.5-turbo-16k" # Switch to 16k context to batch answers

    jsonl_questions = '\n'.join(json.dumps({"question": question, "answer": ""}) for question in questions)

    inputs_data = {
        'article_text': section_txt, 
        'jsonl_questions': jsonl_questions,
        "end_use": task_id_meta["end_use"],
        "answer_tone": task_id_meta["answer_tone"],
        "QA_examples": task_id_meta["QA_examples"]
        }
    
    prompt = build_prompt(prompt_data, inputs_data)
    output = query_openai_chat(prompt, model_name, section_id, estimated_tokens = 5000, req_name = "Answer Extraction")

    jsonl_pattern = r'(?:\{"question":.*?}|{\'question\':.*?})(?:\n|$)' # Match the JSONL format
    jsonl_lines = re.findall(jsonl_pattern, output, flags=re.DOTALL)

    answers = [json.loads(line)["answer"] for line in jsonl_lines]

    if len(answers) == 0:
        raise ValueError(f"No answers generated for section_id : {section_id}")
    
    return answers