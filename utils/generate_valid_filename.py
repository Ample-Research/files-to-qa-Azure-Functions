import re

def generate_valid_filename(filename_no_ext): # without the extension!
    valid_filename = re.sub(r'[\\/*?:"<>|]', "", filename_no_ext)
    valid_filename = valid_filename.replace(" ", "_")
    valid_filename = valid_filename.lower()
    return valid_filename[:255]