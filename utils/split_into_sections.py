import nltk
import logging
from utils.num_tokens_from_string import num_tokens_from_string
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.warning("Downloading Punkt! -- IF THIS IS NOT LOCAL, SOMETHING IS WRONG!")
    nltk.download('punkt')

def split_into_sections(text, max_tokens=3000):
    total_tokens = num_tokens_from_string(text)
    num_sections = total_tokens // max_tokens
    adjusted_max_tokens = total_tokens // (num_sections + 1) if total_tokens % max_tokens else total_tokens // num_sections
    
    sentences = sent_tokenize(text)
    sections = []
    section_tokens = 0
    section_text = ""

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


