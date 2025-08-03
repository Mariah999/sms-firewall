from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from project.apis.keywords.handlers import (
    add_keyword_handler,
    delete_keyword_handler,
    get_keyword_handler,
    get_keywords_handler,
    update_keyword_handler,
)
from project.apis.keywords.models import keyword_model
from project.utilities.autentication import token_required

keyword_namespace = Namespace(
    "keywords", description="Keywords related operations CRUD"
)

keyword_namespace.add_model("Keyword", keyword_model)


class KeywordsList(Resource):
    @token_required
    @keyword_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @keyword_namespace.expect(keyword_model, validate=True)
    @keyword_namespace.response(code=HTTPStatus.CREATED, description="Keyword Inserted")
    def post(self):
        try:
            payload = request.get_json()
            data = {"name": payload["name"]}
            resp_data = add_keyword_handler(data)
            response_object = {"status": "success", "objectId": str(resp_data)}
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            keyword_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    # @token_required
    @keyword_namespace.response(code=HTTPStatus.OK, description="Keywords List found")
    @keyword_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    def get(self):
        resp_data = get_keywords_handler()
        response_object = {"status": "success", "data": resp_data}
        return response_object, HTTPStatus.OK


class Keyword(Resource):
    @token_required
    @keyword_namespace.response(code=HTTPStatus.OK, description="Keyword found")
    @keyword_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Keyword not found"
    )
    @keyword_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    def get(self, keyword_id):
        keyword = get_keyword_handler(keyword_id)
        if not keyword or keyword is None:
            keyword_namespace.abort(HTTPStatus.NOT_FOUND, "Keyword not found")
        else:
            return keyword, HTTPStatus.OK

    @token_required
    @keyword_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @keyword_namespace.expect(keyword_model, validate=True)
    @keyword_namespace.response(code=HTTPStatus.OK, description="Keyword updated")
    @keyword_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Keyword not found"
    )
    @keyword_namespace.response(code=HTTPStatus.BAD_REQUEST, description="Bad request")
    def put(self, keyword_id):
        try:
            payload = request.get_json()
            data = {"name": payload["name"]}
            resp_data = update_keyword_handler(keyword_id, data)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            keyword_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

    @token_required
    @keyword_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @keyword_namespace.response(code=HTTPStatus.OK, description="Keyword deleted")
    @keyword_namespace.response(
        code=HTTPStatus.NOT_FOUND, description="Keyword not found"
    )
    @keyword_namespace.response(code=HTTPStatus.BAD_REQUEST, description="Bad request")
    def delete(self, keyword_id):
        try:
            resp_data = delete_keyword_handler(keyword_id)
            response_object = {"status": "success", "response": str(resp_data)}
            return response_object, HTTPStatus.OK
        except Exception as e:
            keyword_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )


keyword_namespace.add_resource(KeywordsList, "")
keyword_namespace.add_resource(Keyword, "/<string:keyword_id>")
