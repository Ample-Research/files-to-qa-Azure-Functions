import re
import json
import logging

from utils.build_prompt import build_prompt
from utils.query_openai import query_openai_chat

def extract_questions(section_txt, task_id_meta, prompt_data, section_id):
    '''
    This function will take in text and use the OpenAI API to create questions.
    The questions should be reverse engineered and include all beleivable questions answered by the article.
    '''
    input_data = {
        "article_text": section_txt,
        "custom_prompt_q": task_id_meta["custom_prompt_q"],
        "QA_examples": task_id_meta["QA_examples"]
    }
    prompt = build_prompt(prompt_data, input_data)
    output = query_openai_chat(prompt, task_id_meta["model_name"], section_id, estimated_tokens = 500, req_name = "Question Extraction")
    output = output.choices[0].message['content']

    pattern = r'"question"\s*:\s*"([^"]*?)"|\'answer\'\s*:\s*\'([^\']*?)\'' # Match the question text format
    matches = re.findall(pattern, output, flags=re.DOTALL)
    questions = [match[0] if match[0] else match[1] for match in matches]

    if len(questions) == 0:
        raise ValueError(f"No questions generated for section_id : {section_id}")
    
    return questions