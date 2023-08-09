from utils.hardcoded_prompts import hardcoded_prompts

def retrieve_prompt_data(prompt_list, blob_connection_str_secret):
    '''
    TEMPORARY FUNCTION LOGIC!

    TODO: THIS WILL ALL BE CHANGED ONCE THE PROMPT-SCHEMATICS REPO IS ADDED
    '''
    all_prompt_data = []
    for prompt_name in prompt_list:
        this_prompt_data = hardcoded_prompts[prompt_name]
        all_prompt_data.append(this_prompt_data)

    return tuple(all_prompt_data)

    