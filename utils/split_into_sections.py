import nltk
import logging
from utils.num_tokens_from_string import num_tokens_from_string
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.warning("Downloading Punkt! -- IF THIS IS NOT LOCAL, SOMETHING IS WRONG!")
    nltk.download('punkt')

from utils.timeit import timeit

@timeit
def split_into_sections(text, max_tokens=1000, threshhold_ratio = 0.8):
    sections = []
    section_tokens = 0
    section_text = ""
    sentences = sent_tokenize(text)

    total_tokens = num_tokens_from_string(text)
    num_sections = total_tokens // max_tokens
    remaining_tokens = total_tokens % max_tokens
    
    while remaining_tokens > max_tokens * threshhold_ratio: # Even out section sizes
        max_tokens -= 100
        num_sections = total_tokens // max_tokens
        remaining_tokens = total_tokens % max_tokens

    num_sections = total_tokens // max_tokens
    adjusted_max_tokens = total_tokens // (num_sections + 1) if total_tokens % max_tokens else total_tokens // num_sections
  
    for sentence in sentences:

        words = sentence.split()
        while len(words) > 40:
            part_sentence = " ".join(words[:40])
            part_tokens = num_tokens_from_string(part_sentence)
            if section_tokens + part_tokens > adjusted_max_tokens:
                sections.append(section_text)
                section_text = part_sentence
                section_tokens = part_tokens
            else:
                section_text += " " + part_sentence
                section_tokens += part_tokens
            words = words[40:] # Combine the rest of the words

        sentence = " ".join(words)
        sentence_tokens = num_tokens_from_string(sentence)
        if section_tokens + sentence_tokens > adjusted_max_tokens: # Repeat of before with rest of words.
            sections.append(section_text)
            section_text = sentence
            section_tokens = sentence_tokens
        else:
            section_text += " " + sentence
            section_tokens += sentence_tokens

    if section_text:
        sections.append(section_text.strip()) # Add the last section if any

    return sections


