from io import BytesIO
from docx import Document
from pdfminer.high_level import extract_text
from utils.timeit import timeit

@timeit
def extract_text_from_file(raw_file, filename):
    
    # Convert raw file data to a file-like object
    file_stream = BytesIO(raw_file)

    # Extract extension from filename
    extension = filename.split('.')[-1].lower()
    if extension:
        extension = '.' + extension

    # Handle file types
    if extension == ".pdf":
        raw_text = extract_text(file_stream)
    elif extension == ".docx":
        doc = Document(file_stream)
        raw_text = '\n'.join([p.text for p in doc.paragraphs])
    elif extension == ".csv" or extension == ".txt":
        raw_text = file_stream.read().decode('utf-8')
    else:
        raise ValueError("Unsupported file type: " + extension)

    return raw_text