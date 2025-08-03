from datetime import datetime
import json

from project.apis.whitelistednumbers.crud import (
    add_whitelistednumber,
    delete_whitelistednumber,
    get_whitelistednumber,
    get_whitelistednumbers,
    is_senderId_already_exist,
    update_whitelistednumber,
)


def add_whitelistednumber_handler(data):
    if not data.get("senderId") or data.get("senderId") == "":
        raise Exception("senderId is required")
    if is_senderId_already_exist_handler(data["senderId"]):
        print(is_senderId_already_exist_handler(data["senderId"]))
        raise Exception("senderId already exists")
    data["created_at"] = datetime.utcnow()
    whitelistednumber = add_whitelistednumber(data)
    return whitelistednumber


def get_whitelistednumber_handler(whitelistednumber_id):
    res = get_whitelistednumber(whitelistednumber_id)
    if res not in ["null", None]:
        res = json.loads(res)
        res["_id"] = str(res["_id"]["$oid"])
        res["created_at"] = str(res["created_at"]["$date"])
        if res.get("updated_at"):
            res["updated_at"] = str(res["updated_at"]["$date"])
        return res
    else:
        return None


def update_whitelistednumber_handler(whitelistednumber_id, data):
    if not get_whitelistednumber_handler(whitelistednumber_id):
        raise Exception("Whitelistednumber not found")

    if not data.get("senderId") or data.get("senderId") == "":
        raise Exception("senderId is required")

    if is_senderId_already_exist_handler(data["senderId"]):
        print(is_senderId_already_exist_handler(data["senderId"]))
        raise Exception("senderId already exists")

    data["updated_at"] = datetime.utcnow()
    whitelistednumber = update_whitelistednumber(whitelistednumber_id, data)

    return whitelistednumber


def delete_whitelistednumber_handler(whitelistednumber_id):
    if not get_whitelistednumber_handler(whitelistednumber_id):
        raise Exception("Whitelistednumber not found")

    whitelistednumber = delete_whitelistednumber(whitelistednumber_id)
    return whitelistednumber


def get_whitelistednumbers_handler():
    whitelistednumbers = get_whitelistednumbers()
    whitelistednumbers = json.loads(whitelistednumbers)
    for whitelistednumber in whitelistednumbers:
        whitelistednumber["_id"] = str(whitelistednumber["_id"]["$oid"])
        whitelistednumber["created_at"] = str(whitelistednumber["created_at"]["$date"])
        if whitelistednumber.get("updated_at"):
            whitelistednumber["updated_at"] = str(whitelistednumber["updated_at"]["$date"])
    return whitelistednumbers


def is_senderId_already_exist_handler(senderId):
    whitelistednumber = is_senderId_already_exist(senderId)
    return whitelistednumber
