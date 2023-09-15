from utils.timeit import timeit

@timeit
def build_prompt(prompt_data, input_data):
    prompt = prompt_data['prompt']
    inputs = prompt_data["inputs"]
    inputs_list = inputs.split(',')
    for input_name in inputs_list:
            input_name = input_name.strip() # Remove any leading or trailing whitespace
            if input_name in input_data:
                prompt = prompt.replace('{' + input_name + '}', str(input_data[input_name]))
            else:
              raise ValueError(f"Input '{input_name}' not found in inputs_data")
    return prompt
