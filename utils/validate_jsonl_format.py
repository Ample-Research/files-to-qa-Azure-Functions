import json
import re
import logging

def validate_jsonl_format(input_string, task_id):
    cleaned_jsonl_lines = []
    lines = input_string.strip().split('\n')
    for line in lines:
        trimmed_line = line.strip()
        if not trimmed_line: # Skip if the line is empty
          continue
        try:
            json_object = json.loads(trimmed_line)
            if "question" not in json_object or "answer" not in json_object:
                logging.warning(f"Error in {task_id} JSON -- Missing 'question' or 'answer' in line: {line}")
                continue  # Skip this line
            if not json_object["question"].strip() or not json_object["answer"].strip():
                logging.warning(f"Error in {task_id} JSON -- Empty 'question' or 'answer' in line: {line}")
                continue  # Skip this line
            
            esc_single_re = r"(?<!\\)'" # Replace single quote w/ escaped single quote
            esc_double_re = r'(?<!\\)"' # Replace double quote w/ escaped single quote
            json_object["question"] = re.sub(esc_single_re, "\\'", json_object["question"])
            json_object["answer"] = re.sub(esc_single_re, "\\'", json_object["answer"])
            json_object["question"] = re.sub(esc_double_re, "\\'", json_object["question"])
            json_object["answer"] = re.sub(esc_double_re, "\\'", json_object["answer"])

            cleaned_jsonl_lines.append(json.dumps(json_object))
        except json.JSONDecodeError as e:
            logging.error(f"Error in {task_id} JSON -- Invalid JSON object in line: {line}")
            raise e
    return '\n'.join(cleaned_jsonl_lines)
