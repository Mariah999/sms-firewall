from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource
from project.apis.OTP.handlers import add_rule_handler, delete_rule_handler, get_rule_handler, get_rules_handler, update_rule_handler
from project.apis.OTP.crud import del_all
from project.apis.OTP.models import rule_model, update_rule_model
from project.utilities.autentication import token_required

OTP_namespace = Namespace("OTP_namespace", description="OTP related operations CRUD")

OTP_namespace.add_model("Rule", rule_model)
OTP_namespace.add_model("updateRule", update_rule_model)

class RulesList(Resource):
    @token_required
    @OTP_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @OTP_namespace.response(HTTPStatus.OK, description="Rules List found")
    def get(self):
        resp_data = get_rules_handler()
        response_object = {"status": "success", "data": resp_data}
        return response_object, HTTPStatus.OK

    @token_required
    @OTP_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @OTP_namespace.expect(rule_model, validate=True)
    @OTP_namespace.response(HTTPStatus.CREATED, description="Rule Added")
    def post(self):
        try:
            data = request.get_json()
            rule_type = data.get('rule_type')
            category = data.get('category')
            features = data.get('features')
            status = data.get('status', True)
            
            if not (rule_type and category and features):
                return {'message': 'rule_type, category, and features are required'}, HTTPStatus.BAD_REQUEST
            
            resp_data = add_rule_handler(rule_type, category, features, status)
            response_object = {"status": "success", "objectId": str(resp_data)}
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            OTP_namespace.abort(HTTPStatus.BAD_REQUEST, message=str(e), status="error")


    @token_required
    @OTP_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @OTP_namespace.response(HTTPStatus.OK, description="All rules deleted")
    def delete(self):
        try:
            del_all()
            return {"status": "success", "message": "All rules deleted successfully"}, HTTPStatus.OK
        except Exception as e:
            OTP_namespace.abort(HTTPStatus.BAD_REQUEST, message=str(e), status="error")

class Rule(Resource):
    @token_required
    @OTP_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @OTP_namespace.response(HTTPStatus.OK, description="Rule found")
    @OTP_namespace.response(HTTPStatus.NOT_FOUND, description="Rule not found")
    def get(self, rule_id):
        try:
            rule = get_rule_handler(rule_id)
            if rule is None:
                OTP_namespace.abort(HTTPStatus.NOT_FOUND, "Rule not found")
            return {"status": "success", "data": rule}, HTTPStatus.OK
        except Exception as e:
            OTP_namespace.abort(HTTPStatus.BAD_REQUEST, message=str(e), status="error")

    @token_required
    @OTP_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @OTP_namespace.response(HTTPStatus.OK, description="Rule deleted")
    @OTP_namespace.response(HTTPStatus.NOT_FOUND, description="Rule not found")
    def delete(self, rule_id):
        try:
            if delete_rule_handler(rule_id):
                response_object = {"status": "success", 'message': 'Rule deleted successfully'}
                return response_object, HTTPStatus.OK
            else:
                OTP_namespace.abort(HTTPStatus.NOT_FOUND, message="Rule not found")
        except Exception as e:
            print(f"Error in delete method: {e}")  
            OTP_namespace.abort(HTTPStatus.BAD_REQUEST, message=str(e), status="error")

    @token_required
    @OTP_namespace.doc(
        params={
            "Authorization": {
                "in": "header",
                "description": "Authorization token",
                "type": "string",
                "required": True,
            }
        }
    )
    @OTP_namespace.expect(update_rule_model, validate=True)
    @OTP_namespace.response(HTTPStatus.OK, description="Rule updated")
    @OTP_namespace.response(HTTPStatus.NOT_FOUND, description="Rule not found")
    @OTP_namespace.response(HTTPStatus.BAD_REQUEST, description="Invalid input")
    def put(self, rule_id):
        try:
            data = request.get_json()
            rule_type = data.get('rule_type')
            status = data.get('status')
            
            if rule_type is None and status is None:
                return {'message': 'At least one field (rule_type or status) is required to update'}, HTTPStatus.BAD_REQUEST

            updated_rule = update_rule_handler(rule_id, rule_type, status)
            if updated_rule:
                return {"status": "success", "data": updated_rule}, HTTPStatus.OK
            else:
                OTP_namespace.abort(HTTPStatus.NOT_FOUND, "Rule not found")
        except Exception as e:
            OTP_namespace.abort(HTTPStatus.BAD_REQUEST, message=str(e), status="error")

            
OTP_namespace.add_resource(RulesList, "/rules")
OTP_namespace.add_resource(Rule, "/rules/<string:rule_id>")
