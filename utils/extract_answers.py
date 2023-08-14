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
        "custom_prompt_a": task_id_meta["custom_prompt_a"]
        }

    prompt = build_prompt(prompt_data, inputs_data)
    output = query_openai_chat(prompt, "gpt-3.5-turbo-16k", section_id, estimated_tokens=6000, req_name="Answer Extraction", num_choices=3)
    answers = []

    for choice in output.choices:
        
        output_txt = choice.message['content']

        pattern = r'"answer"\s*:\s*"([^"]*?)"|\'answer\'\s*:\s*\'([^\']*?)\'' # Match the answer text format
        matches = re.findall(pattern, output_txt, flags=re.DOTALL)
        answers = [match[0] if match[0] else match[1] for match in matches]

        if len(answers) == len(questions):
            break       
        
        pattern = r'"answer"\s*:\s*("([^"]*?)"|\'([^\']*?)\')' # Try Second Pattern
        matches = re.findall(pattern, output_txt, flags=re.DOTALL)
        answers = [match[0] if match[0] else match[1] for match in matches]

        if len(answers) == len(questions):
            break     

        pattern = r'"answer"\s*:\s*"([^"]*)"' # Try Third Pattern
        matches = re.findall(pattern, output_txt, flags=re.DOTALL)
        answers = [match[0] if match[0] else match[1] for match in matches]

        if len(answers) == len(questions):
            break     

        pattern = r'"answer"\s*:\s*"((?:[^"\\]|\\.)*)"' # Try Fourth Pattern
        matches = re.findall(pattern, output_txt, flags=re.DOTALL)
        answers = [match[0] if match[0] else match[1] for match in matches]

    if len(answers) != len(questions):
        raise ValueError(f"Question and Answer are not the same length!\n Questions: {questions} \n\n Answers: {answers}")

    if len(answers) == 0:
        raise ValueError(f"No answers generated for section_id : {section_id}")
    
    return answers