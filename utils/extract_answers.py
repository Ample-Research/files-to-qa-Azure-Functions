import re

from utils.build_prompt import build_prompt
from utils.query_openai import query_openai

def extract_answers(section_txt, task_id_meta, questions, prompt_data, section_id):
    '''
    This function will take in an blockof txt and a list of questions related to that txt.
    It will then use OpenAI to generate robust answers to those questions using the article.
    It will utilize the prompts stored in `answer_extraction.csv`
    '''
    all_answers = []
    for question in questions:
        inputs_data = {
            'article_text': section_txt, 
            'question': question,
            "end_use": task_id_meta["end_use"],
            "answer_tone": task_id_meta["answer_tone"],
            "QA_examples": task_id_meta["QA_examples"]
            }
        prompt = build_prompt(prompt_data, inputs_data)
        output = query_openai(prompt, task_id_meta["model_name"])

        answer = output.strip().replace('"', "") # Get rid of double quotes
        answer = re.sub(r'^[^a-zA-Z]*', '', answer) # Replace begining characters like dashes or 1.
        all_answers.append(answer)
    
    if len(all_answers) == 0:
        raise ValueError(f"No answers generated for section_id : {section_id}")
    
    return all_answers