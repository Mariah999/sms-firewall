from project import mongo
from bson.objectid import ObjectId

otp_rules_collection = mongo.db["otp_rules"]

def add_rule(data):
    result = otp_rules_collection.insert_one(data)
    return str(result.inserted_id) 

def delete_rule(rule_id):
    result = otp_rules_collection.delete_one({"_id": ObjectId(rule_id)})
    return result.raw_result

def get_existing_patterns(rule_type):
    existing_patterns_cursor = otp_rules_collection.find(
        {'rule_type': rule_type},
        {'regex_pattern': 1, '_id': 0}
    )
    return [pattern['regex_pattern'] for pattern in existing_patterns_cursor]

def get_rules():
    rules = otp_rules_collection.find(
        {},
        {'_id': 1, 'rule_type': 1, 'category': 1, 'regex_pattern': 1, 'logic_text': 1, 'status': 1}
    )
    return list(rules)

def get_rule_by_id(rule_id):
    rule = otp_rules_collection.find_one(
        {'_id': ObjectId(rule_id)},
        {'_id': 0, 'rule_type': 1, 'category': 1, 'regex_pattern': 1, 'logic_text': 1, 'status': 1}
    )
    if rule:
        rule['id'] = str(rule_id)
    return rule

def update_rule(rule_id, update_fields):
    result = otp_rules_collection.update_one(
        {"_id": ObjectId(rule_id)},
        {"$set": update_fields}
    )
    return result

def del_all():
    otp_rules_collection.delete_many({})