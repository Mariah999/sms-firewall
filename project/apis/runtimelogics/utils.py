import re

def generate_regex_for_keywords(keywords):
    escaped_keywords = [re.escape(keyword) for keyword in keywords]
    regex_pattern = '|'.join(escaped_keywords)
    regex_pattern = r'\b(?:' + regex_pattern + r')\b'
    return regex_pattern

def generate_regex_for_specific_characters(special_characters):
    escaped_characters = ''.join(re.escape(char) for char in special_characters)
    regex_pattern = f"[{escaped_characters}]"
    return regex_pattern

def generate_regex_for_specific_emails(emails):
    escaped_emails = [re.escape(email) for email in emails]
    regex_pattern = '|'.join(escaped_emails)
    regex_pattern = f"(?:{regex_pattern})"
    return regex_pattern


def generate_regex_for_min_digits(min_digits):
    regex_pattern = r"\b\d{{" + f"{min_digits}," + r"}}\b"
    return regex_pattern