from bson import json_util
from bson.objectid import ObjectId as ObjectID

from project import mongo

blockednumbers_collection = mongo.db["blockednumbers"]


def add_blockednumber(data):
    result = blockednumbers_collection.insert_one(data)
    return result.inserted_id


def get_blockednumber(blockednumber_id):
    blockednumber = blockednumbers_collection.find_one(
        {"_id": ObjectID(blockednumber_id)}
    )
    return json_util.dumps(blockednumber)


def update_blockednumber(blockednumber_id, data):
    blockednumber = blockednumbers_collection.update_one(
        {"_id": ObjectID(blockednumber_id)}, {"$set": data}
    )
    return blockednumber.raw_result


def delete_blockednumber(blockednumber_id):
    blockednumber = blockednumbers_collection.delete_one(
        {"_id": ObjectID(blockednumber_id)}
    )
    return blockednumber.raw_result


def get_blockednumbers():
    blockednumbers = blockednumbers_collection.find().sort("created_at", -1)
    return json_util.dumps(blockednumbers)


def get_all_senderId_blockednumbers():
    blockednumbers = blockednumbers_collection.find({}, {"senderId": 1, "destStartsWith":1, "_id": 0})
    return json_util.dumps(blockednumbers)


def is_senderId_already_exist_notself(senderId, blockednumber_id):
    return True if blockednumbers_collection.find_one({"senderId": senderId, "_id":{"$ne": ObjectID(blockednumber_id)}}) else False

def is_senderId_already_exist(senderId):
    return True if blockednumbers_collection.find_one({"senderId": senderId}) else False
