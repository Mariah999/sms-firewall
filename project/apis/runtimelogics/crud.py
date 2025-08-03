from bson import json_util
from bson.objectid import ObjectId as ObjectID

from project import mongo

runtimelogics_collection = mongo.db["runtimelogics"]


def add_runtimelogic(data):
    result = runtimelogics_collection.insert_one(data)
    return result.inserted_id


def get_runtimelogic(runtimelogic_id):
    runtimelogic = runtimelogics_collection.find_one({"_id": ObjectID(runtimelogic_id)})
    return json_util.dumps(runtimelogic)


def update_runtimelogic(runtimelogic_id, data):
    runtimelogic = runtimelogics_collection.update_one(
        {"_id": ObjectID(runtimelogic_id)}, {"$set": data}
    )
    return runtimelogic.raw_result


def delete_runtimelogic(runtimelogic_id):
    runtimelogic = runtimelogics_collection.delete_one(
        {"_id": ObjectID(runtimelogic_id)}
    )
    return runtimelogic.raw_result


def get_runtimelogics():
    runtimelogics = runtimelogics_collection.find().sort("created_at", -1)
    return json_util.dumps(runtimelogics)


def get_all_active_regex_code():
    runtimelogics = runtimelogics_collection.find(
        {"status": "active"}, {"regex_code": 1, "logictext":1, "_id": 0}
    )
    return json_util.dumps(runtimelogics)
