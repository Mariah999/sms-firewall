from datetime import datetime
import json

from project.apis.runtimelogics.crud import (
    add_runtimelogic,
    delete_runtimelogic,
    get_runtimelogic,
    get_runtimelogics,
    update_runtimelogic,
)


def add_runtimelogic_handler(data):
    if not data.get("logictext") or data.get("logictext") == "":
        raise Exception("LogicText is required")
    data["created_at"] = datetime.utcnow()
    data["status"] = "inactive"
    data["regex_code"] = "Edit to add regex"
    runtime_logic = add_runtimelogic(data)
    return runtime_logic


def get_runtimelogic_handler(runtimelogic_id):
    res = get_runtimelogic(runtimelogic_id)
    if res not in ["null", None]:
        res = json.loads(res)
        res["_id"] = str(res["_id"]["$oid"])
        res["created_at"] = str(res["created_at"]["$date"])
        if res.get("updated_at"):
            res["updated_at"] = str(res["updated_at"]["$date"])
        return res
    else:
        return None


def update_logictext_handler(runtimelogic_id, data):
    if not get_runtimelogic_handler(runtimelogic_id):
        raise Exception("Runtime Logic not found")

    if not data.get("logictext") or data.get("logictext") == "":
        raise Exception("LogicText is required")
    data["updated_at"] = datetime.utcnow()
    res = update_runtimelogic(runtimelogic_id, data)
    if res not in ["null", None]:
        return res
    else:
        return None


def update_regex_code_handler(runtime_logic_id, data):
    if not get_runtimelogic_handler(runtime_logic_id):
        raise Exception("Runtime Logic not found")

    if not data.get("regex_code") or data.get("regex_code") == "":
        raise Exception("regex_code is required")
    data["updated_at"] = datetime.utcnow()
    res = update_runtimelogic(runtime_logic_id, data)
    if res not in ["null", None]:
        return res
    else:
        return None


def update_status_handler(runtime_logic_id, data):
    if not get_runtimelogic_handler(runtime_logic_id):
        raise Exception("Runtime Logic not found")

    if not data.get("status") or data.get("status") == "":
        raise Exception("Status is required")
    data["updated_at"] = datetime.utcnow()
    res = update_runtimelogic(runtime_logic_id, data)
    if res not in ["null", None]:
        return res
    else:
        return None


def delete_runtimelogic_handler(runtimelogic_id):
    if not get_runtimelogic_handler(runtimelogic_id):
        raise Exception("Runtime Logic not found")

    runtime_logic = delete_runtimelogic(runtimelogic_id)
    return runtime_logic


def get_runtimelogics_handler():
    runtimelogics = get_runtimelogics()
    runtimelogics = json.loads(runtimelogics)
    for runtime_logic in runtimelogics:
        runtime_logic["_id"] = str(runtime_logic["_id"]["$oid"])
        runtime_logic["created_at"] = str(runtime_logic["created_at"]["$date"])
        if runtime_logic.get("updated_at"):
            runtime_logic["updated_at"] = str(runtime_logic["updated_at"]["$date"])

    return runtimelogics


def update_runtimelogic_handler(runtime_logic_id, data):
    if not get_runtimelogic_handler(runtime_logic_id):
        raise Exception("Runtime Logic not found")

    if not data.get("regex_code") or data.get("regex_code") == "":
        raise Exception("regex_code is required")

    if not data.get("logictext") or data.get("logictext") == "":
        raise Exception("LogicText is required")
    data["updated_at"] = datetime.utcnow()
    res = update_runtimelogic(runtime_logic_id, data)
    if res not in ["null", None]:
        return res
    else:
        return None
