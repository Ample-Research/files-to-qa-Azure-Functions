import re

from utils.build_prompt import build_prompt
from utils.query_openai import query_openai

def extract_questions(section_txt, task_id_meta, prompt_data, section_id):
    '''
    This function will take in text and use the OpenAI API to create questions.
    The questions should be reverse engineered and include all beleivable questions answered by the article.
    '''
    input_data = {
        "article_text": section_txt,
        "end_use": task_id_meta["end_use"],
        "QA_examples": task_id_meta["QA_examples"]
    }
    prompt = build_prompt(prompt_data, input_data)
    output = query_openai(prompt, task_id_meta["model_name"])

    questions = output.strip().replace('"', "").replace('- ', "") # Clean out double quotes and dashes
    questions = questions.split('\n') # Split into list based on \n
    questions = list(filter(None, questions)) # Filter out questions with no text
    questions = [re.sub(r'^[^a-zA-Z]*', '', question) for question in questions] # Clean questions beginning with 1. 2. 3....

    if len(questions) == 0:
        raise ValueError(f"No questions generated for section_id : {section_id}")
    
    return questions