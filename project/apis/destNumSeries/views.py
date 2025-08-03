from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from project.apis.destNumSeries.handlers import (
    add_destNumSeries_handler,
    delete_destNumSeries_handler,
    get_all_destNumSeries_handler,
    get_destNumSeries_handler,
    update_destNumSeries_handler,
)
from project.apis.destNumSeries.models import dest_num_series_model
from project.utilities.autentication import token_required

destNumSeries_namespace = Namespace(
    "destNumSeries", description="Destination Number Series related operations CRUD"
)

destNumSeries_namespace.add_model("DestNumSeries", dest_num_series_model)

class DestNumSeriesList(Resource):
    @token_required
    @destNumSeries_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @destNumSeries_namespace.expect(dest_num_series_model, validate=True)
    @destNumSeries_namespace.response(
        code=HTTPStatus.CREATED, description="DestNumSeries Inserted"
    )
    def post(self):
        try:
            payload = request.get_json()
            data = {"startsWith": payload["startsWith"]}
            resp_data = add_destNumSeries_handler(data)
            response_object = {"status": "success", "objectId": str(resp_data)}
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            destNumSeries_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @destNumSeries_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @destNumSeries_namespace.response(
        code=HTTPStatus.OK, description="All DestNumSeries"
    )
    def get(self):
        try:
            resp_data = get_all_destNumSeries_handler()
            return resp_data, HTTPStatus.OK
        except Exception as e:
            destNumSeries_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

class DestNumSeries(Resource):
    @token_required
    @destNumSeries_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @destNumSeries_namespace.response(
        code=HTTPStatus.OK, description="DestNumSeries found"
    )
    @destNumSeries_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="DestNumSeries not found"
    )
    def get(self, destNumSeries_id):
        try:
            resp_data = get_destNumSeries_handler(destNumSeries_id)
            if resp_data:
                return resp_data, HTTPStatus.OK
            else:
                return {"status": "failed", "message": "DestNumSeries not found"}, HTTPStatus.NOT_FOUND
        except Exception as e:
            destNumSeries_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @destNumSeries_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @destNumSeries_namespace.expect(dest_num_series_model, validate=True)
    @destNumSeries_namespace.response(
        code=HTTPStatus.OK, description="DestNumSeries updated"
    )
    @destNumSeries_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="DestNumSeries not found"
    )
    @destNumSeries_namespace.response(
        code=HTTPStatus.BAD_REQUEST, description="Bad request"
    )
    def put(self, destNumSeries_id):
        try:
            payload = request.get_json()
            data = {"startsWith": payload["startsWith"]}
            resp_data = update_destNumSeries_handler(destNumSeries_id, data)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            destNumSeries_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )
    
    @token_required
    @destNumSeries_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @destNumSeries_namespace.response(
        code=HTTPStatus.OK, description="DestNumSeries deleted"
    )
    @destNumSeries_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="DestNumSeries not found"
    )
    def delete(self, destNumSeries_id):
        try:
            resp_data = delete_destNumSeries_handler(destNumSeries_id)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            destNumSeries_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

destNumSeries_namespace.add_resource(DestNumSeriesList, "")
destNumSeries_namespace.add_resource(DestNumSeries, "/<destNumSeries_id>")