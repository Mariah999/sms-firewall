from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from project.apis.blockednumbers.handlers import (
    add_blockednumber_handler,
    delete_blockednumber_handler,
    get_blockednumber_handler,
    get_blockednumbers_handler,
    update_blockednumber_handler,
)
from project.apis.blockednumbers.models import blockednumber_model
from project.utilities.autentication import token_required

blockednumber_namespace = Namespace(
    "blockednumbers", description="Blockednumbers related operations CRUD"
)

blockednumber_namespace.add_model("Blockednumber", blockednumber_model)


class BlockednumbersList(Resource):
    @token_required
    @blockednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @blockednumber_namespace.expect(blockednumber_model, validate=True)
    @blockednumber_namespace.response(
        code=HTTPStatus.CREATED, description="Blockednumber Inserted"
    )
    def post(self):
        try:
            payload = request.get_json()
            if payload.get("destStartsWith"):
                data = {
                    "senderId": payload["senderId"],
                    "destStartsWith": payload["destStartsWith"],
                }
            else:
                data = {
                    "senderId": payload["senderId"]
                }
            resp_data = add_blockednumber_handler(data)
            response_object = {"status": "success", "objectId": str(resp_data)}
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            blockednumber_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @blockednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @blockednumber_namespace.response(
        code=HTTPStatus.OK, description="Blockednumbers List found"
    )
    def get(self):
        resp_data = get_blockednumbers_handler()
        response_object = {"status": "success", "data": resp_data}
        return response_object, HTTPStatus.OK


class Blockednumber(Resource):
    @token_required
    @blockednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @blockednumber_namespace.response(
        code=HTTPStatus.OK, description="Blockednumber found"
    )
    @blockednumber_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Blockednumber not found"
    )
    def get(self, blockednumber_id):
        blockednumber = get_blockednumber_handler(blockednumber_id)
        if not blockednumber or blockednumber is None:
            blockednumber_namespace.abort(
                HTTPStatus.NOT_FOUND, "Blockednumber not found"
            )
        else:
            return blockednumber, HTTPStatus.OK

    @token_required
    @blockednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @blockednumber_namespace.expect(blockednumber_model, validate=True)
    @blockednumber_namespace.response(
        code=HTTPStatus.OK, description="Blockednumber updated"
    )
    @blockednumber_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Blockednumber not found"
    )
    @blockednumber_namespace.response(
        code=HTTPStatus.BAD_REQUEST, description="Bad request"
    )
    def put(self, blockednumber_id):
        try:
            payload = request.get_json()
            if payload.get("destStartsWith"):
                data = {
                    "senderId": payload["senderId"],
                    "destStartsWith": payload["destStartsWith"],
                }
            else:
                data = {
                    "senderId": payload["senderId"],
                    "destStartsWith": []
                }
            resp_data = update_blockednumber_handler(blockednumber_id, data)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            blockednumber_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @blockednumber_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @blockednumber_namespace.response(
        code=HTTPStatus.OK, description="Blockednumber deleted"
    )
    @blockednumber_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Blockednumber not found"
    )
    def delete(self, blockednumber_id):
        try:
            resp_data = delete_blockednumber_handler(blockednumber_id)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            blockednumber_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )


blockednumber_namespace.add_resource(BlockednumbersList, "")
blockednumber_namespace.add_resource(Blockednumber, "/<string:blockednumber_id>")
