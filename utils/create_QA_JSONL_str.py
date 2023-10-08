import json
import logging
from utils.timeit import timeit

@timeit
def create_QA_JSONL_str(questions, answers, task_id_meta, section_id):

    if len(questions) != len(answers):
        raise ValueError(f"Failed to create JSONL for section: {section_id} -- Questions and answers must be the same length! (Q: {len(questions)}  A: {len(answers)})")

    start_sequence = task_id_meta["start_sequence"]
    stop_sequence = task_id_meta["stop_sequence"]

    jsonl_str = ""
    for q, a in zip(questions, answers):
        obj = {
            "question": q + start_sequence,
            "answer": a + stop_sequence
        }
        jsonl_str += json.dumps(obj) + "\n"

    return jsonl_str