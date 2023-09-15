from utils.upload_to_blob import upload_to_blob

def trigger_sections(sections, task_id, blob_connection_str_secret, queue_connection_str_secret):
  
  for idx, section in enumerate(sections):
    this_section_id = f"{task_id}_section_{str(idx)}"
    upload_to_blob(section, blob_connection_str_secret,"file-sections", this_section_id)
    # Upload section status "initiated" to a section table
    # Upload "this_section_id" to a new process_section queue
    upload_to_table() # Not implemented
  
  return True