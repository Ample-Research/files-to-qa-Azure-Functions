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

    jsonl_questions = '\n'.join(json.dumps({"question": question, "answer": ""}) for question in questions)

    inputs_data = {
        'article_text': section_txt, 
        'jsonl_questions': jsonl_questions,
        "end_use": task_id_meta["end_use"],
        "answer_tone": task_id_meta["answer_tone"],
        "QA_examples": task_id_meta["QA_examples"]
        }

    retries = 4
    for _ in range(retries):
        prompt = build_prompt(prompt_data, inputs_data)
        output = query_openai_chat(prompt, "gpt-3.5-turbo-16k", section_id, estimated_tokens=5000, req_name="Answer Extraction")

        pattern = r'"answer"\s*:\s*"([^"]*?)"|\'answer\'\s*:\s*\'([^\']*?)\'' # Match the answer text format
        matches = re.findall(pattern, output, flags=re.DOTALL)
        answers = [match[0] if match[0] else match[1] for match in matches]

        if len(answers) == len(questions):
            break       
        
        pattern = r'"answer"\s*:\s*("([^"]*?)"|\'([^\']*?)\')' # Try Second Pattern
        matches = re.findall(pattern, output, flags=re.DOTALL)
        answers = [match[0] if match[0] else match[1] for match in matches]

        if len(answers) == len(questions):
            break     

        pattern = r'"answer"\s*:\s*"([^"]*)"' # Try Third Pattern
        matches = re.findall(pattern, output, flags=re.DOTALL)
        answers = [match[0] if match[0] else match[1] for match in matches]

        if len(answers) == len(questions):
            break     

        pattern = r'"answer"\s*:\s*"((?:[^"\\]|\\.)*)"' # Try Fourth Pattern
        matches = re.findall(pattern, output, flags=re.DOTALL)
        answers = [match[0] if match[0] else match[1] for match in matches]

    if len(answers) != len(questions):
        pattern = r'"answer"'
        count = len(re.findall(pattern, output))
        raise ValueError(f"Question and Answer are not the same length! The word 'answer' appeared {count} in final output for {len(questions)} number of questions.")

    if len(answers) == 0:
        raise ValueError(f"No answers generated for section_id : {section_id}")
    
    return answers