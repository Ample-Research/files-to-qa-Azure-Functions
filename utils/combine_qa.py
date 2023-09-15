from utils.upload_to_blob import upload_to_blob
from utils.combine_JSONL import combine_JSONL
from utils.generate_blob_download_link import generate_blob_download_link
from utils.generate_valid_filename import generate_valid_filename
from utils.timeit import timeit

@timeit
def combine_qa(task_id, num_sections, title, blob_connection_str_secret, table_connection_str_secret):
    section_ids = []
    for idx in range(num_sections):
        section_ids.append(f"{task_id}_section_{idx}_jsonl")
    final_jsonl_str = combine_JSONL(task_id, section_ids, blob_connection_str_secret)
    final_file_id = "{task_id}_final"
    upload_to_blob(final_jsonl_str, blob_connection_str_secret, "final-processed-results", final_file_id)

    download_filename = generate_valid_filename(title) + ".jsonl"
    download_link = generate_blob_download_link(blob_connection_str_secret, "final-processed-results", final_file_id, download_filename)

    return download_link