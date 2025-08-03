from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from project.apis.runtimelogics.handlers import (
    add_runtimelogic_handler,
    delete_runtimelogic_handler,
    get_runtimelogic_handler,
    get_runtimelogics_handler,
    update_logictext_handler,
    update_regex_code_handler,
    update_runtimelogic_handler,
    update_status_handler,
)
from project.apis.runtimelogics.models import (
    logic_text_and_regex_code_model,
    logic_text_model,
    regex_code_model,
    status_model,
)
from project.utilities.autentication import token_required

runtimelogic_namespace = Namespace(
    "runtimelogics", description="Runtime Logics related operations"
)

runtimelogic_namespace.add_model("LogicText", logic_text_model)
runtimelogic_namespace.add_model("RegexCode", regex_code_model)
runtimelogic_namespace.add_model("Status", status_model)
runtimelogic_namespace.add_model("LogicTextAndRegexCode", logic_text_and_regex_code_model)


class RuntimelogicsList(Resource):
    @token_required
    @runtimelogic_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @runtimelogic_namespace.expect(logic_text_model, validate=True)
    @runtimelogic_namespace.response(
        code=HTTPStatus.CREATED, description="LogicText Inserted"
    )
    def post(self):
        try:
            payload = request.get_json()
            data = {"logictext": payload["logictext"]}
            resp_data = add_runtimelogic_handler(data)
            response_object = {"status": "success", "objectId": str(resp_data)}
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            runtimelogic_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @runtimelogic_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.OK, description="Runtime Logics List found"
    )
    def get(self):
        resp_data = get_runtimelogics_handler()
        response_object = {"status": "success", "data": resp_data}
        return response_object, HTTPStatus.OK


class RuntimeLogic(Resource):
    @token_required
    @runtimelogic_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @runtimelogic_namespace.expect(logic_text_and_regex_code_model, validate=True)
    @runtimelogic_namespace.response(
        code=HTTPStatus.OK, description="Runtime Logic updated"
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Runtime Logic not found"
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.BAD_REQUEST, description="Bad request"
    )
    def put(self, runtimelogic_id):
        try:
            payload = request.get_json()
            data = {"logictext": payload["logictext"], "regex_code": payload["regex_code"]}
            resp_data = update_runtimelogic_handler(runtimelogic_id, data)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            runtimelogic_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @runtimelogic_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.OK, description="Runtime Logic found"
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Runtime Logic not found"
    )
    def get(self, runtimelogic_id):
        runtimelogic = get_runtimelogic_handler(runtimelogic_id)
        if not runtimelogic or runtimelogic is None:
            runtimelogic_namespace.abort(
                HTTPStatus.NOT_FOUND, "Runtime Logic not found"
            )
        else:
            return runtimelogic, HTTPStatus.OK

    @token_required
    @runtimelogic_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.OK, description="Runtime Logic deleted"
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Runtime Logic not found"
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.BAD_REQUEST, description="Bad request"
    )
    def delete(self, runtimelogic_id):
        try:
            resp_data = delete_runtimelogic_handler(runtimelogic_id)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            runtimelogic_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )


class LogicText(Resource):
    @token_required
    @runtimelogic_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @runtimelogic_namespace.expect(logic_text_model, validate=True)
    @runtimelogic_namespace.response(
        code=HTTPStatus.OK, description="LogicText updated"
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Runtime Logic not found"
    )
    @runtimelogic_namespace.response(
        code=HTTPStatus.BAD_REQUEST, description="Bad request"
    )
    def put(self, runtimelogic_id):
        try:
            payload = request.get_json()
            data = {"logictext": payload["logictext"]}
            resp_data = update_logictext_handler(runtimelogic_id, data)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            runtimelogic_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )


class RegexCode(Resource):
    @token_required
    @runtimelogic_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @runtimelogic_namespace.expect(regex_code_model, validate=True)
    @runtimelogic_namespace.response(
        code=HTTPStatus.OK, description="regex_code updated"
    )
    def put(self, runtimelogic_id):
        try:
            payload = request.get_json()
            data = {"regex_code": payload["regex_code"]}
            resp_data = update_regex_code_handler(runtimelogic_id, data)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            runtimelogic_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )


class Status(Resource):
    @token_required
    @runtimelogic_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @runtimelogic_namespace.expect(status_model, validate=True)
    @runtimelogic_namespace.response(code=HTTPStatus.OK, description="Status updated")
    def put(self, runtimelogic_id):
        try:
            payload = request.get_json()
            data = {"status": payload["status"]}
            resp_data = update_status_handler(runtimelogic_id, data)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            runtimelogic_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )


runtimelogic_namespace.add_resource(RuntimelogicsList, "")
runtimelogic_namespace.add_resource(RuntimeLogic, "/<string:runtimelogic_id>")
runtimelogic_namespace.add_resource(LogicText, "/<string:runtimelogic_id>/logictext")
runtimelogic_namespace.add_resource(RegexCode, "/<string:runtimelogic_id>/regexcode")
runtimelogic_namespace.add_resource(Status, "/<string:runtimelogic_id>/status")
