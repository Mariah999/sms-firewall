from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from project.apis.validatesms.handlers import check_regex_handler, validatesms_handler
from project.apis.validatesms.models import test_sms_model, validatesms_model
from project.utilities.autentication import token_required, check_internal_api_key

validatesms_namespace = Namespace("validatesms", description="Validatesms a sms.")

validatesms_namespace.add_model("Validatesms", validatesms_model)
validatesms_namespace.add_model("TestSms", test_sms_model)


class Validatesms(Resource):
    # for frontend api uncomment token_required
    # for only only validating sms uncomment check_internal_api_key
    @token_required
    @check_internal_api_key
    @validatesms_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @validatesms_namespace.expect(validatesms_model, validate=True)
    @validatesms_namespace.response(code=HTTPStatus.OK, description="The sms is valid")
    @validatesms_namespace.response(
        code=HTTPStatus.BAD_REQUEST, description="The the request is invalid."
    )
    def post(self):
        try:
            payload = request.get_json()
            data = {
                    "senderId": payload["senderId"], 
                    "message": payload["message"],
                    "destinationNumber": payload["destinationNumber"]
                }
            resp_data = validatesms_handler(data)
            if resp_data["status"] == "success":
                return resp_data, HTTPStatus.ACCEPTED
            else:
                return resp_data, HTTPStatus.NOT_ACCEPTABLE

        except Exception as e:
            validatesms_namespace.abort(
                HTTPStatus.BAD_REQUEST, message=str(e), status="error"
            )

class TestSms(Resource):
    @token_required
    @validatesms_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        },
    )
    @validatesms_namespace.expect(test_sms_model, validate=True)
    @validatesms_namespace.response(code=HTTPStatus.OK, description="This regex can succussfully block this sms")
    @validatesms_namespace.response(
        code=HTTPStatus.NOT_ACCEPTABLE, description="This regex cannot block this sms"
    )
    def post(self, runtimelogic_id):
        payload = request.get_json()
        if check_regex_handler(payload["message"], runtimelogic_id):
            response_object = {"status": "success", "message": "This regex can succussfully block this sms"}
            return response_object, HTTPStatus.OK
        else:
            response_object = {"status": "failed", "message": "This regex cannot block this sms"}
            return response_object, HTTPStatus.NOT_ACCEPTABLE

validatesms_namespace.add_resource(Validatesms, "")
validatesms_namespace.add_resource(TestSms, "/test/<runtimelogic_id>") # comment this line for only validating sms
