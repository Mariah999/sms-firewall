from flask_restx import Model, fields

validatesms_model = Model(
    "Validatesms",
    {
        "senderId": fields.String(
            required=True, description="Sender Id", example="senderId"
        ),
        "message": fields.String(
            required=True, description="Message", example="message"
        ),
        "destinationNumber": fields.String(
            required=True, description="Destination Mobile Number", example="8801712345678"
        ),
    },
)

test_sms_model = Model(
    "TestSms",
    {
        "message": fields.String(
            required=True, description="Message", example="message"
        ),
    },
)
