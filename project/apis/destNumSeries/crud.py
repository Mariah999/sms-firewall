from bson import json_util
from bson.objectid import ObjectId as ObjectID

from project import mongo

destNumSeries_collection = mongo.db["destNumSeries"]

def add_destNumSeries(data):
    result = destNumSeries_collection.insert_one(data)
    return result.inserted_id

def get_destNumSeries(destNumSeries_id):
    destNumSeries = destNumSeries_collection.find_one(
        {"_id": ObjectID(destNumSeries_id)}
    )
    return json_util.dumps(destNumSeries)

def update_destNumSeries(destNumSeries_id, data):
    destNumSeries = destNumSeries_collection.update_one(
        {"_id": ObjectID(destNumSeries_id)}, {"$set": data}
    )
    return destNumSeries.raw_result

def delete_destNumSeries(destNumSeries_id):
    destNumSeries = destNumSeries_collection.delete_one(
        {"_id": ObjectID(destNumSeries_id)}
    )
    return destNumSeries.raw_result

def get_all_destNumSeries():
    destNumSeries = destNumSeries_collection.find().sort("created_at", -1)
    return json_util.dumps(destNumSeries)

def get_all_startsWith_destNumSeries():
    destNumSeries = destNumSeries_collection.find({}, {"startsWith": 1, "_id": 0})
    return json_util.dumps(destNumSeries)

def is_destNumSeries_already_exist(startsWith):
    return True if destNumSeries_collection.find_one({"startsWith": startsWith}) else False