import nltk
import os
from nltk.tokenize import sent_tokenize
nltk.data.path.append(os.path.join(os.path.dirname("resources/nltk_data"), "resources", "nltk_data"))

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