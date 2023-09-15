import os
import logging
import openai
import time
from tenacity import retry, wait_random_exponential, retry_if_exception_type

from utils.num_tokens_from_string import num_tokens_from_string


openai.api_type = "azure"
openai.api_base = "https://files-to-qa-openai.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv('OPEN_AI_KEY')


def retry_callback(retry_state):
    ''' Callback function for logging retry attempts '''
    exception = retry_state.outcome.exception()
    logging.warning(f"Retrying due to: {exception} - Attempt {retry_state.attempt_number}")

@retry(wait=wait_random_exponential(multiplier=1, min=2, max=20), retry_error_callback=retry_callback, retry=retry_if_exception_type(Exception), reraise=True)
def query_openai_chat(prompt, model_name, section_id, estimated_tokens = 1000, req_name = "Unnamed", num_choices = 1):
    '''
    Queries OpenAI.
    To Do: Add more parameters eventually.
    '''
    logging.info(f"Begin {req_name} request to OpenAI -- Section: {section_id}")

    try:

        prompt_tokens = num_tokens_from_string(prompt)
        if model_name == "qa-gpt-35-4k-context" and prompt_tokens + estimated_tokens > 4000:
            message = f"Inputted prompt was too long to be precessed in section {section_id}! Prompt Tokens: {prompt_tokens}"
            logging.error(message)
            raise ValueError(message) # This will not trigger a retry

        initial_message = [{"role": "user", "content": prompt}]
        completion = openai.ChatCompletion.create(
            engine=model_name,
            messages=initial_message,
            max_tokens=estimated_tokens,
            n = num_choices
        )
        logging.info(f"Completed OpenAI {req_name} Request (Finish Reason {completion.choices[0]['finish_reason']})  -- Section: {section_id} -- OpenAI ID: {completion['id']} -- OpenAI Info: {completion['usage']} -- Estimated Tokens: {estimated_tokens}")
        return completion
    
    except ValueError as e:
        raise # Do not retry, raise it to the caller

    except Exception as e:
        message = f"Error while Querying OpenAI {req_name} Request  -- Section: {section_id}: {str(e)}."
        logging.error(message)
        raise Exception(message) # This will trigger a retry