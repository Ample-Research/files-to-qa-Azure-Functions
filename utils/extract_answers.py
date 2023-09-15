import re
import json
import time
import logging

from utils.build_prompt import build_prompt
from utils.query_openai import query_openai_chat
from utils.timeit import timeit

@timeit
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
    output = query_openai_chat(prompt, "qa-gpt-35-16k-context", section_id, estimated_tokens=6000, req_name="Answer Extraction", num_choices=3)
    answers, answer_choice = regex_ops(output, questions)

    if answer_choice is None or len(answers) != len(questions):
        raise ValueError(f"Question and Answer lengths mismatch!\n Questions: {questions} \n\n Answers: {answers}")

    if not answers:
        raise ValueError(f"No answers generated for section_id : {section_id}")

    return answers, answer_choice, output.usage["completion_tokens"]


@timeit
def regex_ops(output, questions):
    answers = []
    patterns = [
        r'"answer"\s*:\s*"([^"]*?)"|\'answer\'\s*:\s*\'([^\']*?)\'',
        r'"answer"\s*:\s*("([^"]*?)"|\'([^\']*?)\')',
        r'"answer"\s*:\s*"([^"]*)"',
        r'"answer"\s*:\s*"((?:[^"\\]|\\.)*)"'
    ]

    for idx, choice in enumerate(output.choices):
        output_txt = choice.message['content']
        answer_choice = idx
        for pattern in patterns:
            matches = re.findall(pattern, output_txt, flags=re.DOTALL)

            try:
                answers = [match[0] if match[0] else match[1] for match in matches]
            except IndexError:
                continue

            if len(answers) == len(questions):
                answer_choice = idx
                break
            
        if answer_choice is not None:
            break

    return answers, answer_choice