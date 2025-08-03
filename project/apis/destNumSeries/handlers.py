from datetime import datetime
import json

from project.apis.destNumSeries.crud import (
    add_destNumSeries,
    get_destNumSeries,
    update_destNumSeries,
    delete_destNumSeries,
    get_all_destNumSeries,
    is_destNumSeries_already_exist
)

def add_destNumSeries_handler(data):
    if not data.get("startsWith") or data.get("startsWith") == "":
        raise Exception("startsWith number is required")
    if is_destNumSeries_already_exist(data["startsWith"]):
        print(is_destNumSeries_already_exist(data["startsWith"]))
        except_str = f"startsWith {data['startsWith']} already exists"
        raise Exception(except_str)
    data["created_at"] = datetime.utcnow()
    destNumSeries = add_destNumSeries(data)
    return destNumSeries

def get_destNumSeries_handler(destNumSeries_id):
    res = get_destNumSeries(destNumSeries_id)
    if res not in ["null", None]:
        res = json.loads(res)
        res["_id"] = str(res["_id"]["$oid"])
        res["created_at"] = str(res["created_at"]["$date"])
        if res.get("updated_at"):
            res["updated_at"] = str(res["updated_at"]["$date"])
        return res
    else:
        return None
    
def update_destNumSeries_handler(destNumSeries_id, data):
    if not get_destNumSeries_handler(destNumSeries_id):
        raise Exception("DestNumSeries not found")

    if not data.get("startsWith") or data.get("startsWith") == "":
        raise Exception("startsWith is required")

    if is_destNumSeries_already_exist_handler(data["startsWith"]):
        print(is_destNumSeries_already_exist_handler(data["startsWith"]))
        raise Exception("startsWith already exists")

    data["updated_at"] = datetime.utcnow()
    destNumSeries = update_destNumSeries(destNumSeries_id, data)

    return destNumSeries

def delete_destNumSeries_handler(destNumSeries_id):
    if not get_destNumSeries_handler(destNumSeries_id):
        raise Exception("DestNumSeries not found")

    destNumSeries = delete_destNumSeries(destNumSeries_id)
    return destNumSeries

def get_all_destNumSeries_handler():
    res = get_all_destNumSeries()
    if res not in ["null", None]:
        res = json.loads(res)
        for r in res:
            r["_id"] = str(r["_id"]["$oid"])
            r["created_at"] = str(r["created_at"]["$date"])
            if r.get("updated_at"):
                r["updated_at"] = str(r["updated_at"]["$date"])
        return res
    else:
        return None
    
def is_destNumSeries_already_exist_handler(startsWith):
    return True if is_destNumSeries_already_exist(startsWith) else False