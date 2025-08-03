from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from project.apis.whitelistednumbers.handlers import (
    add_whitelistednumber_handler,
    delete_whitelistednumber_handler,
    get_whitelistednumber_handler,
    get_whitelistednumbers_handler,
    update_whitelistednumber_handler,
)
from project.apis.whitelistednumbers.models import whitelistednumber_model
from project.utilities.autentication import token_required

whitelistednumber_namespace = Namespace(
    "whitelistednumbers", description="Whitelistednumbers related operations CRUD"
)

whitelistednumber_namespace.add_model("Whitelistednumber", whitelistednumber_model)


class WhitelistednumbersList(Resource):
    @token_required
    @whitelistednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @whitelistednumber_namespace.expect(whitelistednumber_model, validate=True)
    @whitelistednumber_namespace.response(
        code=HTTPStatus.CREATED, description="Whitelistednumber Inserted"
    )
    def post(self):
        try:
            payload = request.get_json()
            data = {"senderId": payload["senderId"]}
            resp_data = add_whitelistednumber_handler(data)
            response_object = {"status": "success", "objectId": str(resp_data)}
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            whitelistednumber_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @whitelistednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @whitelistednumber_namespace.response(
        code=HTTPStatus.OK, description="Whitelistednumbers List found"
    )
    def get(self):
        resp_data = get_whitelistednumbers_handler()
        response_object = {"status": "success", "data": resp_data}
        return response_object, HTTPStatus.OK


class Whitelistednumber(Resource):
    @token_required
    @whitelistednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @whitelistednumber_namespace.response(
        code=HTTPStatus.OK, description="Whitelistednumber found"
    )
    @whitelistednumber_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Whitelistednumber not found"
    )
    def get(self, whitelistednumber_id):
        whitelistednumber = get_whitelistednumber_handler(whitelistednumber_id)
        if not whitelistednumber or whitelistednumber is None:
            whitelistednumber_namespace.abort(
                HTTPStatus.NOT_FOUND, "Whitelistednumber not found"
            )
        else:
            return whitelistednumber, HTTPStatus.OK

    @token_required
    @whitelistednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @whitelistednumber_namespace.expect(whitelistednumber_model, validate=True)
    @whitelistednumber_namespace.response(
        code=HTTPStatus.OK, description="Whitelistednumber updated"
    )
    @whitelistednumber_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Whitelistednumber not found"
    )
    @whitelistednumber_namespace.response(
        code=HTTPStatus.BAD_REQUEST, description="Bad request"
    )
    def put(self, whitelistednumber_id):
        try:
            payload = request.get_json()
            data = {"senderId": payload["senderId"]}
            resp_data = update_whitelistednumber_handler(whitelistednumber_id, data)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            whitelistednumber_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @whitelistednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @whitelistednumber_namespace.response(
        code=HTTPStatus.OK, description="Whitelistednumber deleted"
    )
    @whitelistednumber_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Whitelistednumber not found"
    )
    def delete(self, whitelistednumber_id):
        try:
            resp_data = delete_whitelistednumber_handler(whitelistednumber_id)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            whitelistednumber_namespace.abort(
                HTTPStatus.NOT_FOUND, message=str(e), status="error"
            )


whitelistednumber_namespace.add_resource(WhitelistednumbersList, "")
whitelistednumber_namespace.add_resource(
    Whitelistednumber, "/<string:whitelistednumber_id>"
)
