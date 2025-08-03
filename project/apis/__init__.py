from flask_restx import Api

from project.apis.alive.api import alive_namespace
from project.apis.blockednumbers.views import blockednumber_namespace
from project.apis.keywords.views import keyword_namespace
from project.apis.runtimelogics.views import runtimelogic_namespace
from project.apis.validatesms.views import validatesms_namespace
from project.apis.whitelistednumbers.views import whitelistednumber_namespace
from project.apis.destNumSeries.views import destNumSeries_namespace
from project.apis.OTP.views import OTP_namespace

api = Api(
    version="1.0",
    title="sms-firewall-service APIs",
    prefix="/api/firewall/v1",
    doc="/api/firewall/v1/docs",
)

api.add_namespace(alive_namespace, path="/alive")
api.add_namespace(keyword_namespace, path="/keywords")
api.add_namespace(whitelistednumber_namespace, path="/whitelistednumbers")
api.add_namespace(blockednumber_namespace, path="/blockednumbers")
api.add_namespace(runtimelogic_namespace, path="/runtimelogics")
api.add_namespace(destNumSeries_namespace, path="/destnumseries")
api.add_namespace(OTP_namespace, path="/otp")
api.add_namespace(validatesms_namespace, path="/validatesms") # this should be uncommented for while validating sms and other should be commented
