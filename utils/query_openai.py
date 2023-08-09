import logging
import openai
import time

from utils.num_tokens_from_string import num_tokens_from_string

def query_openai(prompt, model_name, retries=5, type_of_call="NoType"):
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

    for i in range(retries):
        try:
            completion = openai.ChatCompletion.create(
                model=model_name,
                messages=initial_message,
                max_tokens=min(max_tokens, 1500)
            )
            result = completion.choices[0].message['content']
            return result
        except Exception as e:
            if i < retries - 1:  # i is zero indexed
                wait_t = 2 ** i  # exponential backoff
                logging.warning(f"Error while Querying OpenAI: {e}. Retrying in {wait_t} seconds.")
                time.sleep(wait_t)
            else:
                message = f"Failed OpenAI Query after {retries} retries."
                logging.error(message)
                raise ValueError(message)