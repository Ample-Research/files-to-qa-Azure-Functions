import nltk
import logging
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.warning("Downloading Punkt! -- IF THIS IS NOT LOCAL, SOMETHING IS WRONG!")
    nltk.download('punkt')

def split_into_sections(text, max_words=1500, threshold_ratio=0.2):
    sentences = sent_tokenize(text)
    sections = []
    words = []

    for sentence in sentences:
        sentence_words = sentence.split()
        if len(words) + len(sentence_words) > max_words:
            # Check if next section would be too small compared to this one
            if len(words) / (len(words) + len(sentence_words)) < threshold_ratio:
                # Append this sentence to the current section if next one would be too small
                words.extend(sentence_words)
            else:
                # Otherwise, start a new section
                sections.append(' '.join(words))
                words = sentence_words
        else:
            words.extend(sentence_words)

    # Add the last section if any
    if words:
        sections.append(' '.join(words))

    return sections