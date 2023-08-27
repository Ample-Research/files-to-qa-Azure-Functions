from utils.read_from_blob import read_from_blob
from utils.validate_jsonl_format import validate_jsonl_format

def combine_JSONL(task_id, section_ids, blob_connection_str_secret):
    completed_section_ids = [key + "_jsonl" for key, value in section_ids.items() if value == "completed"]
    combined_jsonl = ""
    for jsonl_section_id in completed_section_ids:
        section_content_bytes = read_from_blob(blob_connection_str_secret, "file-sections", jsonl_section_id)
        combined_jsonl += section_content_bytes.decode('utf-8') + "\n"
    final_jsonl_str = validate_jsonl_format(combined_jsonl, task_id)
    return final_jsonl_str
