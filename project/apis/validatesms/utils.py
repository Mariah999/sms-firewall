import re

otp_type_sms_keywords = {
    "code": 2, "pin": 2, "otp": 3, "otp is:": 3, "otp is :": 3, "otp is -": 3, "otp is-": 3, "code is:": 3, "code is :": 3, "code is -": 3, "code is-": 3, "login otp": 2,
    "verification": 1, "authentication": 1, "credential": 1, "password": 2, "reference": 1, "number": 1, "vrn": 1, "login": 1, "confirmation": 1, "secret": 1, "security code": 2,
    "auth code": 2, "কোড": 2, "পিন": 2, "ওটিপি": 3, "লগইন ওটিপি": 2, "যাচাইকরণ": 1, "প্রমাণীকরণ": 1, "শংসাপত্র": 1, "পাসওয়ার্ড": 2, "রেফারেন্স": 1, "নম্বর": 1, "ভিআরএন": 1, "লগইন": 1,
    "নিশ্চিতকরণ": 1, "নতুন পাসওয়ার্ড": 1, "গোপন": 1
}

def retrieve_url(text):
    pattern = r'(?:[A-Za-z0-9\-]+\.[A-Za-z]{2,}|' \
              r'(?:http|ftp)s?://' \
              r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' \
              r'localhost|' \
              r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' \
              r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' \
              r'(?::\d+)?' \
              r'(?:/?|[/?]\S+))'

    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        if re.search(r'\.\w{2,3}$', match.group()):
            return match.group()
        else:
            return None
    else:
        return None


def remove_urls(text):
    detected_url = retrieve_url(text)
    if detected_url:
        text = re.sub(re.escape(detected_url), '', text)
    return text


def score_sentences(text):
    sentence_regex = re.compile(r'([^.!?]*(?:\b\w*\d{3,}\w*\b)[^.!?]*)', re.M)
    sentences = sentence_regex.findall(text)
    sentence_scores = []
    for sentence in sentences:
        score = sum(otp_type_sms_keywords.get(keyword.lower(), 0) for keyword in otp_type_sms_keywords if keyword.lower() in sentence.lower())
        if score > 0:
            sentence_scores.append((score, sentence))

    if not sentence_scores:
        return None

    best_sentence = max(sentence_scores, key=lambda x: x[0])[1]
    return best_sentence


def find_closest_chunk(digit_chunks, best_sentence):
    keyword_positions = {}
    for keyword, weight in otp_type_sms_keywords.items():
        if keyword.lower() in best_sentence.lower():
            keyword_positions[keyword.lower()] = best_sentence.lower().find(keyword.lower())

    closest_chunk = None
    min_weighted_distance = float('inf')

    for chunk in digit_chunks:
        chunk_position = best_sentence.find(chunk)
        for keyword, position in keyword_positions.items():
            distance = abs(chunk_position - position)
            weighted_distance = distance / otp_type_sms_keywords[keyword]
            if weighted_distance < min_weighted_distance:
                min_weighted_distance = weighted_distance
                closest_chunk = chunk
    return closest_chunk


def extract_otp(text):
    text = remove_urls(text)
    best_sentence = score_sentences(text)
    if not best_sentence:
        return None

    # digit_chunks = re.findall(r'\b\w*[\w@-]*\d{4,}\b', best_sentence)
    digit_chunks = re.findall(r'[a-zA-Z]*[-+@]?\d+[a-zA-Z]*[-+@]?\d*', best_sentence)
    if len(digit_chunks) == 1:
        return digit_chunks[0]

    closest_chunk = find_closest_chunk(digit_chunks, best_sentence)
    return closest_chunk