def process_section_batch(batch, context, prompt_data, task_id):
    parallel_tasks = [context.call_activity("PROCESS_SECTION", {
                "section_id": section_id, 
                "task_id": task_id,
                "prompt_data": prompt_data
            }) for section_id, status in batch if status != "completed"]
    return parallel_tasks if parallel_tasks else []