from datetime import datetime
import json

from project.apis.blockednumbers.crud import (
    add_blockednumber,
    delete_blockednumber,
    get_blockednumber,
    get_blockednumbers,
    is_senderId_already_exist,
    update_blockednumber,
    is_senderId_already_exist_notself
)


def add_blockednumber_handler(data):
    if not data.get("senderId") or data.get("senderId") == "":
        raise Exception("senderId is required")
    if is_senderId_already_exist_handler(data["senderId"]):
        print(is_senderId_already_exist_handler(data["senderId"]))
        raise Exception("senderId already exists")
    data["created_at"] = datetime.utcnow()
    blockednumber = add_blockednumber(data)
    return blockednumber


def get_blockednumber_handler(blockednumber_id):
    res = get_blockednumber(blockednumber_id)
    if res not in ["null", None]:
        res = json.loads(res)
        res["_id"] = str(res["_id"]["$oid"])
        res["created_at"] = str(res["created_at"]["$date"])
        if res.get("updated_at"):
            res["updated_at"] = str(res["updated_at"]["$date"])
        if not res.get("destStartsWith"):
            res["destStartsWith"] = []
        return res
    else:
        return None


def update_blockednumber_handler(blockednumber_id, data):
    if not get_blockednumber_handler(blockednumber_id):
        raise Exception("Blockednumber not found")

    if not data.get("senderId") or data.get("senderId") == "":
        raise Exception("senderId is required")

    if is_senderId_already_exist_notself_handler(data["senderId"], blockednumber_id):
        print(is_senderId_already_exist_notself_handler(data["senderId"], blockednumber_id))
        raise Exception("senderId already exists")

    data["updated_at"] = datetime.utcnow()
    blockednumber = update_blockednumber(blockednumber_id, data)

    return blockednumber


def delete_blockednumber_handler(blockednumber_id):
    if not get_blockednumber_handler(blockednumber_id):
        raise Exception("Blockednumber not found")

    blockednumber = delete_blockednumber(blockednumber_id)
    return blockednumber


def get_blockednumbers_handler():
    blockednumbers = get_blockednumbers()
    blockednumbers = json.loads(blockednumbers)
    for blockednumber in blockednumbers:
        blockednumber["_id"] = str(blockednumber["_id"]["$oid"])
        blockednumber["created_at"] = str(blockednumber["created_at"]["$date"])
        if blockednumber.get("updated_at"):
            blockednumber["updated_at"] = str(blockednumber["updated_at"]["$date"])
        if not blockednumber.get("destStartsWith"):
            blockednumber["destStartsWith"] = []
    return blockednumbers


def is_senderId_already_exist_notself_handler(senderId, blockednumber_id):
    return True if is_senderId_already_exist_notself(senderId, blockednumber_id) else False

def is_senderId_already_exist_handler(senderId):
    return True if is_senderId_already_exist(senderId) else False
