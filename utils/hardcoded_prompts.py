def hardcoded_prompts(prompt_name):
    prompt_data = {}


# QUESTION EXTRACTION PROMPT --------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------
    if prompt_name == "question_extraction":
        
        prompt_data["prompt"] = """<!-- Begin Instructions -->
Your task is to analyze the provided document and generate a list of pertinent questions that the information in the document answers. Your questions should be formulated based on the guidelines given below, be relevant to the document's conent, and mimic the variability of human language.

Guidelines:
{custom_prompt_q}
---
Now, analyze the following document and generate as many pertinent questions as possible.
Here is the document:
<!-- End Instructions -->
<!-- Begin Document -->
{article_text}
<!-- End Document -->
<!-- Begin Final Call To Action -->
Please format your questions as JSONL like this:
{"question":"QUESTION_A"}
{"question":"QUESTION_B"}
{"question":"QUESTION_C"}
...
Feel free to provide as many pertinent questions as you can within the given format.
<!-- End Final Call To Action -->"""
        prompt_data["inputs"] = "article_text, custom_prompt_q"


# ANSWER EXTRACTION PROMPT ----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------
    elif prompt_name == "answer_extraction":
        
        prompt_data["prompt"] = """<!-- Begin Instructions --> 
Your task is to analyze the provided document and answer the provided questions related to the content of the document. Each question should be considered, and you are to delve into the document to extract the information necessary to answer it. Your responses must align with the guidelines and tone given below.

Guidelines:
{custom_prompt_a}

Here is the document:
<!-- End Instructions --> 
<!-- Begin Document --> 
{article_text} 
<!-- End Document --> 
<!-- Begin Final Call To Action -->
Answer ALL of the following questions in the given format, adhering to the tone and guidelines provided above. Maintain the same JSONL format in your response:

{jsonl_questions}

<!-- End Final Call To Action -->
"""
        prompt_data["inputs"] = "article_text, jsonl_questions, custom_prompt_a"


# TAGS EXTRACTION PROMPT ----------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
    elif prompt_name == "topic_tags_extraction":
        
        prompt_data["prompt"] = """<!-- Begin Instructions -->
As an advanced NLP model, you possess the capability to grasp the subtle nuances and overarching themes within a piece of text. In this task, you are to analyze an article and extract a comprehensive list of topic tags that encompass the scope of the document. The topics tags should be exhaustive and diverse, capturing both broad themes and specific sub-topics contained within the document. 

While the primary themes are important, the subtle, perhaps less dominant aspects can often be the key to understanding the complexity of the document. Aim to generate a robust set of tags, erring on the side of more is better, as these tags will be used to facilitate a more accurate and precise categorization of document and serve as basis for future model training. 

Now, proceed with the following document: 
<!-- End Instructions --> 
<!-- Begin Document --> 
{article_text}
 <!-- End Document --> 

<!-- Begin Final Call To Action -->
Analyze its content and generate a comprehensive, detailed list of topic tags. Please output the tags in a comma seperated list, using underscores (_) instead of spaces like this: [tag_1,tag_2,...] 
<!-- End Final Call To Action -->
"""
        prompt_data["inputs"] = "article_text"

    return prompt_data
