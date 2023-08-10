import re
import logging

from utils.build_prompt import build_prompt
from utils.query_openai import query_openai

def extract_topic_tags(section_txt, task_id_meta, prompt_data, section_id):
    inputs_data = {'article_text': section_txt}
    prompt = build_prompt(prompt_data, inputs_data)
    output = query_openai(prompt, task_id_meta["model_name"])
    match = re.search('\[(.*?)\]', output) # Search string for "[tagA, tagB, ...]" and extract
    if match:
        tags_str = match.group(1)
        tags = [tag.strip() for tag in tags_str.split(",")] # Clean tags and convert to list
    else:
      tags = []
      logging.warning(f"Pattern not found in output -- No Tags for section: {section_id}")

    return tags