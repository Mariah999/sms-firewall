from datetime import datetime
import json

from project.apis.keywords.crud import (
    add_keyword,
    delete_keyword,
    get_keyword,
    get_keywords,
    update_keyword,
)


def add_keyword_handler(data):
    if not data.get("name") or data.get("name") == "":
        raise Exception("Name is required")
    data["created_at"] = datetime.utcnow()
    data["name"] = data["name"].lower()
    keyword = add_keyword(data)
    return keyword


def get_keyword_handler(keyword_id):
    keyword = get_keyword(keyword_id)
    if keyword not in ["null", None]:
        keyword = json.loads(keyword)
        keyword["_id"] = str(keyword["_id"]["$oid"])
        keyword["created_at"] = str(keyword["created_at"]["$date"])
        if keyword.get("updated_at"):
            keyword["updated_at"] = str(keyword["updated_at"]["$date"])
        return keyword
    else:
        return None


def update_keyword_handler(keyword_id, data):
    if not get_keyword_handler(keyword_id):
        raise Exception("Keyword not found")

    if not data.get("name") or data.get("name") == "":
        raise Exception("Name is required")

    data["updated_at"] = datetime.utcnow()
    data["name"] = data["name"].lower()
    keyword = update_keyword(keyword_id, data)

    return keyword


def delete_keyword_handler(keyword_id):
    if not get_keyword_handler(keyword_id):
        raise Exception("Keyword not found")

    keyword = delete_keyword(keyword_id)
    return keyword


def get_keywords_handler():
    keywords = get_keywords()
    keywords = json.loads(keywords)
    for keyword in keywords:
        keyword["_id"] = str(keyword["_id"]["$oid"])
        keyword["created_at"] = str(keyword["created_at"]["$date"])
        if keyword.get("updated_at"):
            keyword["updated_at"] = str(keyword["updated_at"]["$date"])
    return keywords
