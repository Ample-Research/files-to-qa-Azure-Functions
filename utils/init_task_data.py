import datetime

def init_task_data(task_id, config_data, file_size_in_bytes, filename):
    '''
    The goal of this function is to initialize the metadata for a new task (e.g. file-upload).
    It will take in the task_id and create a JSON dictionary that will track the task across its lifecycle.
    '''

    task_id_meta_data = {
        # Core Meta Data
        "task_id": task_id,
        "raw_file_id": f"{task_id}_raw",
        "raw_text_id": f"{task_id}_txt",
        "final_output_id": f"{task_id}_final",
        "user_id": config_data.get("user_id"),
        # Processing Config
        "title": config_data.get("title"),
        "tags": config_data.get("tags"),
        "end_use": config_data["end_use"],
        "answer_tone": config_data["answer_tone"],
        "QA_examples": config_data["QA_examples"],
        "model_name": config_data["model_name"],
        "start_sequence": config_data["start_sequence"],
        "stop_sequence": config_data["stop_sequence"],
        # Status Tracking
        "status": "initiated",
        "section_tracker": {},
        "date_created": str(datetime.datetime.now()),
        "error_message": None,
        "num_QA_pairs": 0,
        "processing_time": 0,
        "file_size_in_bytes": file_size_in_bytes,
        "filename": filename
    }
    
    return task_id_meta_data


'''
EXAMPLE CONFIG DATA JSON OBJECT:

{
    "user_id": "TESTUSER",
    "title": "Statistics Randomization TEST",
    "tags": ["stats", "report", "math"],
    "end_use": "I want to make a Q&A model that knows all about statistics to help me in my job as a data scientist.",
    "answer_tone": "It should be technical and smart. A critical thinker.",
    "QA_examples":[
      "Explain the dangers of Selecting on the Dependent Variable.\n\nIf you only look at instances when a phenomenon occured, you are trying to assess correlation without variation. You must have variations to make comparisons.",
      "Why does causation not imply correlation?\n\nTake an example, fire-fighters are highly correlated with fire damage, but clearly they don't cause fires.",
      "Why are counter-examples like 'I got the flu shot last year and I still got the flu' not a valid critique of average effects?\n\nBecasue the evidence is talking about average effects. For example, imagine there are three kinds of people: always sick, never sick, and vaccine responders. Even though the vaccine will improve odds for some, there are some who will still always get sick!"
        ]
}

'''