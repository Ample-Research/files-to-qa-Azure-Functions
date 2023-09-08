from utils.upload_to_blob import upload_to_blob
from utils.combine_JSONL import combine_JSONL
from utils.generate_blob_download_link import generate_blob_download_link
from utils.generate_valid_filename import generate_valid_filename

def combine_qa(task_id_meta, blob_connection_str_secret):
    task_id = task_id_meta["task_id"]
    final_jsonl_str = combine_JSONL(task_id, task_id_meta["section_tracker"], blob_connection_str_secret)
    final_file_id = task_id_meta["final_output_id"]
    upload_to_blob(final_jsonl_str, blob_connection_str_secret, "final-processed-results", final_file_id)
    download_filename = generate_valid_filename(task_id_meta["title"]) + ".jsonl"
    download_link = generate_blob_download_link(blob_connection_str_secret, "final-processed-results", final_file_id, download_filename)

    return download_link