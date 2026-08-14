import re


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not Found"


def extract_phone(text):
    match = re.search(r'\b\d{10}\b', text)
    return match.group(0) if match else "Not Found"


def extract_name(text):
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:
            return line

    return "Not Found"