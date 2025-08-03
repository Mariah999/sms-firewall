import re

def regex_length(length, comparison):
    if comparison == 'greater than':
        pattern = r'^\d{' + str(length + 1) + r',}$'
    elif comparison == 'less than':
        pattern = r'^\d{1,' + str(length - 1) + r'}$'
    elif comparison == 'equal to':
        pattern = r'^\d{' + str(length) + r'}$'
    else:
        raise ValueError("Invalid comparison. Use 'greater than', 'less than', or 'equal to'.")
    return pattern


def regex_sequence(sequence, comparison):
    escaped_sequence = re.escape(sequence)
    if comparison == 'starts with':
        pattern = r'^' + escaped_sequence
    elif comparison == 'ends with':
        pattern = escaped_sequence + r'$'
    elif comparison == 'contain':
        pattern = r'.*' + escaped_sequence + r'.*'
    else:
        raise ValueError("Invalid comparison. Use 'starts with', 'ends with', 'contains'.")
    return pattern


def generate_regex(category, features):
    if category == 'length':
        pattern = regex_length(features['length'], features['comparison'])
    elif category == 'sequence':
        pattern = regex_sequence(features['sequence'], features['comparison'])
    else:
        raise ValueError("Invalid category. Use 'length' or 'sequence'.")
    return pattern

