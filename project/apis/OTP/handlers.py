from datetime import datetime
from flask import current_app as app
from http import HTTPStatus
from flask import abort
from project.apis.OTP.crud import add_rule, delete_rule, get_existing_patterns, get_rule_by_id, get_rules, update_rule
from project.apis.OTP.utils import generate_regex


def get_rules_handler():
    rules = get_rules()
    return [
        {
            'id': str(rule.get('_id')),
            'rule_type': rule.get('rule_type'),
            'category' : rule.get('category'),
            'regex_pattern': rule.get('regex_pattern'),
            'logic_text' : rule.get('logic_text'),
            'status': rule.get('status')
        } for rule in rules
    ]

def add_rule_handler(rule_type, category, features, status=True):
    regex_pattern = generate_regex(category, features)
    existing_patterns = get_existing_patterns(rule_type)

    if regex_pattern is None or regex_pattern == '':
        abort(HTTPStatus.BAD_REQUEST, description='Invalid regex pattern generated.')

    if regex_pattern in existing_patterns:
        abort(HTTPStatus.CONFLICT, description='Regex Pattern already exists!')
    
    logic_text = f"{category} {features['comparison']} {features[category]}"

    data = {
        'created_at': datetime.utcnow(),
        'rule_type': rule_type,
        'category': category,
        'regex_pattern': regex_pattern,
        'logic_text' : logic_text,
        'status': status
    }
    
    rule_id = add_rule(data) 
    
    return {'id': str(rule_id)}



def delete_rule_handler(rule_id):
    result = delete_rule(rule_id)
    return result.get('n', 0) == 1


def get_rule_handler(rule_id):
    rule = get_rule_by_id(rule_id)
    if not rule:
        return None
    return {
        'id': str(rule.get('id')),
        'rule_type': rule.get('rule_type'),
        'category' : rule.get('category'),
        'regex_pattern': rule.get('regex_pattern'),
        'logic_text': rule.get('logic_text'),
        'status': rule.get('status')
    }


def update_rule_handler(rule_id, rule_type=None, status=None):
    update_fields = {}
    if rule_type is not None:
        update_fields['rule_type'] = rule_type
    if status is not None:
        update_fields['status'] = status

    if not update_fields:
        abort(HTTPStatus.BAD_REQUEST, description="No fields provided for update.")

    try:
        result = update_rule(rule_id, update_fields)
        if result.matched_count == 1:
            return get_rule_handler(rule_id)
        else:
            return None
    except Exception as e:
        app.logger.info(f"Error updating rule: {e}")
        return None