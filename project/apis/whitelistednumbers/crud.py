from bson import json_util
from bson.objectid import ObjectId as ObjectID

from project import mongo

whitelistednumbers_collection = mongo.db["whitelistednumbers"]


def add_whitelistednumber(data):
    result = whitelistednumbers_collection.insert_one(data)
    return result.inserted_id


def get_whitelistednumber(whitelistednumber_id):
    whitelistednumber = whitelistednumbers_collection.find_one(
        {"_id": ObjectID(whitelistednumber_id)}
    )
    return json_util.dumps(whitelistednumber)


def update_whitelistednumber(whitelistednumber_id, data):
    whitelistednumber = whitelistednumbers_collection.update_one(
        {"_id": ObjectID(whitelistednumber_id)}, {"$set": data}
    )
    return whitelistednumber.raw_result


def delete_whitelistednumber(whitelistednumber_id):
    whitelistednumber = whitelistednumbers_collection.delete_one(
        {"_id": ObjectID(whitelistednumber_id)}
    )
    return whitelistednumber.raw_result


def get_whitelistednumbers():
    whitelistednumbers = whitelistednumbers_collection.find().sort("created_at", -1)
    return json_util.dumps(whitelistednumbers)


def get_all_senderId_whitelistednumbers():
    whitelistednumbers = whitelistednumbers_collection.find(
        {}, {"senderId": 1, "_id": 0}
    )
    return json_util.dumps(whitelistednumbers)


def is_senderId_already_exist(senderId):
    whitelistednumber = whitelistednumbers_collection.find_one({"senderId": senderId})
    if whitelistednumber:
        return True
    else:
        return False
