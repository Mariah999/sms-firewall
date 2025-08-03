import json
import re

from project.apis.OTP.crud import get_rules
from project.apis.blockednumbers.crud import get_all_senderId_blockednumbers
from project.apis.keywords.crud import get_all_keywords
from project.apis.runtimelogics.crud import get_all_active_regex_code
from project.apis.runtimelogics.handlers import get_runtimelogic_handler
from project.apis.whitelistednumbers.crud import get_all_senderId_whitelistednumbers
from project.apis.destNumSeries.crud import get_all_startsWith_destNumSeries
from project.apis.validatesms.utils import extract_otp


def validatesms_handler(data):
    if data.get("senderId") is None or data.get("senderId") == "":
        response_data = {
            "status": "error",
            "data": {},
            "message": "The senderId is required",
        }
        return response_data

    if data.get("message") is None or data.get("message") == "":
        response_data = {
            "status": "error",
            "data": {},
            "message": "The message is required",
        }
        return response_data
    
    if data.get("destinationNumber") is None or data.get("destinationNumber") == "":
        response_data = {
            "status": "error",
            "data": {},
            "message": "The 13 digits destinationNumber is required",
        }
        return response_data
    
    if len(data.get("destinationNumber")) != 13:
        response_data = {
            "status": "error",
            "data": {},
            "message": "Destination number should be exactly 13 digits.",
        }
        return response_data

    res_status, res_message = check_blockednumber_handler(data["senderId"], data["destinationNumber"])

    if res_status:
        response_data = {
            "status": "failed",
            "data": {
                "senderId": data["senderId"],
            },
            "message": res_message,
        }
        return response_data
    
    if check_destNumSeries(data["destinationNumber"]):
        response_data = {
            "status": "failed",
            "data": {
                "senderId": data["senderId"],
                "message": data["message"],
                "destinationNumber": data["destinationNumber"],
            },
            "message": "The destinationNumber series is blocked",
        }
        return response_data

    whitelisted_numbers = get_all_senderId_whitelistednumbers()
    whitelisted_numbers = json.loads(whitelisted_numbers)
    whitelisted_numbers_set = set()

    for whitelisted_number in whitelisted_numbers:
        whitelisted_numbers_set.add(whitelisted_number["senderId"])

    if data["senderId"] in whitelisted_numbers_set:
        response_data = {
            "status": "success",
            "data": {
                "senderId": data["senderId"],
                "message": data["message"],
            },
            "message": "The senderId is whitelisted",
        }
        return response_data

    keywords = get_all_keywords()
    keywords = json.loads(keywords)
    if check_keywords(data["message"], keywords):
        response_data = {
            "status": "failed",
            "data": {
                "senderId": data["senderId"],
                "message": data["message"],
            },
            "message": "The message contains a unsupported word.",
        }
        return response_data

    regexes = get_all_active_regex_code()
    regexes = json.loads(regexes)

    for regex in regexes:
        pattern = regex["regex_code"]
        if bool(re.search(pattern, data["message"])):
            response_data = {
                "status": "failed",
                "data": {
                    "senderId": data["senderId"],
                    "message": data["message"],
                },
                "message": f"The reason of failure '{regex['logictext']}' ",
            }
            return response_data
        

    otp = extract_otp(data["message"])
    
    if otp and check_invalid_otp(otp):
        response_data = {
            "status": "failed",
            "data": {
                "senderId": data["senderId"],
                "message": data["message"],
            },
            "message": "The message contains a Invalid OTP.",
        }
        return response_data

    response_data = {
        "status": "success",
        "data": {
            "senderId": data["senderId"],
            "message": data["message"],
        },
        "message": "The sms is valid",
    }
    return response_data


def get_separated_rules_handler():
    rules = get_rules()
    block_rules = [rule['regex_pattern'] for rule in rules if rule['rule_type'] == 'block' and rule['status'] == True]
    pass_rules = [rule['regex_pattern'] for rule in rules if rule['rule_type'] == 'pass' and rule['status'] == True]
    return block_rules, pass_rules


def check_invalid_otp(otp):
    block_rules, pass_rules = get_separated_rules_handler()
    for pattern in pass_rules:
        if re.search(pattern, otp):
            return False
    for pattern in block_rules:
        if re.search(pattern, otp):
            return True
    return False

def check_keywords(message, keywords):
    message = message.lower()
    for keyword in keywords:
        if keyword.get("name") and keyword.get("name") in message:
            return True
    return False

def check_regex_handler(message, runtimelogic_id):
    res = get_runtimelogic_handler(runtimelogic_id)
    if res not in ["null", None]:
        if res.get("regex_code") and bool(re.search(res["regex_code"], message)):
            return True
    else:
        return False
    
def check_destNumSeries(destinationNumber):
    destNumSeries = get_all_startsWith_destNumSeries()
    destNumSeries = json.loads(destNumSeries)
    for destNum in destNumSeries:
        if destinationNumber.startswith(destNum["startsWith"]):
            return True
    return False

def check_blockednumber_handler(senderId, destinationNumber):
    blocked_numbers = get_all_senderId_blockednumbers()
    blocked_numbers = json.loads(blocked_numbers)

    for blocked_number in blocked_numbers:
        if blocked_number["senderId"] == senderId:
            if blocked_number.get("destStartsWith") and len(blocked_number["destStartsWith"]) > 0:
                for destStartsWith in blocked_number["destStartsWith"]:
                    if destinationNumber.startswith(destStartsWith):
                        return (True, f"The senderId is blocked for this {destStartsWith} series")
            else:
                return (True, "The senderId is blocked")
    return (False, "The senderId is not blocked")