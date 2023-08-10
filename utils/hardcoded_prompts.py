def hardcoded_prompts(prompt_name):
    prompt_data = {}


# QUESTION EXTRACTION PROMPT --------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------
    if prompt_name == "question_extraction":
        
        prompt_data["prompt"] = """<!-- Begin Instructions --> 
You are an advanced NLP model entrusted with transforming any type of document into a dynamic dataset to train a Q&A language model. Your task is to identify potential questions that the information in the document answers and formulate these questions in a manner a real user might ask them, given the specified end use of the Q&A model. 

The end use of the Q&A modeil is described as follows: 
{end_use} 

To guide you, here are a few examples that illustrate the expected Q&A output (note, for now you are only generating a list of questions): 
{QA_examples} 

Your challenge is to mimic the variability of human language, keeping the questions focused and relevant to the document's content, and in line with the user's preferred end use. Don't shy away from complex or multi-faceted queries. Now, analyze the following article and generate as many pertinent questions as possible: 

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
<!-- End Final Call To Action -->
"""
        prompt_data["inputs"] = "article_text, end_use, QA_examples"


# ANSWER EXTRACTION PROMPT ----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------
    elif prompt_name == "answer_extraction":
        
        prompt_data["prompt"] = """<!-- Begin Instructions --> 
As an advanced NLP model, you have the capacity to extract key information from complex text and communicate it as if you are an expert on the subject. This is your task now. Having been given a list of questions related to the document provided below, your next responsibility is to find the answers. You should consider each question asked and delve into the document to extract the information necessary to answer it. The document could be from any field. Your responses should align with the tone requested below. 

The desired tone for your responses is: 
{answer_tone} 

While extracting information, keep in mind that your responses should not sound as if directly taken from the article. You are to respond as a knowledgeable expert in the field, according to the provided tone. 

Here are a few examples of Question-Answer pairs to help guide you: 
{QA_examples} 

Ultimately, your answers will be used to train a Q&A language model thats end use is as follows: 
{end_use} 

Here are the questions you must answer: 
{jsonl_questions}

Here is the document:
<!-- End Instructions --> 
<!-- Begin Document --> 
{article_text} 
<!-- End Document --> 
<!-- Begin Final Call To Action -->
Please provide well-informed, comprehensive, and engaging answers to the questions. Maintain the same JSONL format in your response.
<!-- End Final Call To Action -->
"""
        prompt_data["inputs"] = "article_text, jsonl_questions, end_use, answer_tone, QA_examples"


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
