def split_into_section_batches(task_metadata, CONCURRENT_LIMIT = 10):
    section_tracker = task_metadata["section_tracker"]
    items_list = list(section_tracker.items())
    section_batches = [items_list[i:i + CONCURRENT_LIMIT] for i in range(0, len(items_list), CONCURRENT_LIMIT)]
    return section_batches