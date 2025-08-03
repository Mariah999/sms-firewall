from bson import json_util
from bson.objectid import ObjectId as ObjectID

from project import mongo

keywords_collection = mongo.db["keywords"]


def add_keyword(data):
    result = keywords_collection.insert_one(data)
    return result.inserted_id


def get_keyword(keyword_id):
    keyword = keywords_collection.find_one({"_id": ObjectID(keyword_id)})
    return json_util.dumps(keyword)


def update_keyword(keyword_id, data):
    keyword = keywords_collection.update_one(
        {"_id": ObjectID(keyword_id)}, {"$set": data}
    )
    return keyword.raw_result


def delete_keyword(keyword_id):
    keyword = keywords_collection.delete_one({"_id": ObjectID(keyword_id)})
    return keyword.raw_result


def get_keywords():
    keywords = keywords_collection.find().sort("created_at", -1)
    return json_util.dumps(keywords)


def get_all_keywords():
    keywords = keywords_collection.find({}, {"name": 1, "_id": 0})
    return json_util.dumps(keywords)
