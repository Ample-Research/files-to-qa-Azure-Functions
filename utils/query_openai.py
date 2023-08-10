import os
import logging
import openai
import time
from tenacity import retry, wait_exponential

from utils.num_tokens_from_string import num_tokens_from_string

openai.api_key = os.getenv('OPEN_AI_KEY')

@retry(wait=wait_exponential(multiplier=1, min=2, max=100))
def query_openai(prompt, model_name):
    '''
    Queries OpenAI.
    To Do: Add more parameters eventually.
    '''

    num_tokens = num_tokens_from_string(prompt)
    max_tokens = (4000 - num_tokens) # Tokenize to avoid breaking request with too large of a token request

    if max_tokens < 0:
        message = "Prompt was too long to be precessed! Max_Tokens < 0"
        logging.error(message)
        raise ValueError(message)

    initial_message = [{"role": "user", "content": prompt}]

    try:
        completion = openai.ChatCompletion.create(
            model=model_name,
            messages=initial_message,
            max_tokens=min(max_tokens, 1500)
        )
        result = completion.choices[0].message['content']
        return result
    except Exception as e:
        message = f"Error while Querying OpenAI: {str(e)}."
        logging.error(message)
        raise ValueError(message)