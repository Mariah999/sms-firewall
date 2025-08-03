from flask_restx import Model, fields

whitelistednumber_model = Model(
    "Whitelistednumber",
    {
        "senderId": fields.String(
            required=True, description="Sender Id", example="senderId"
        ),
    },
)
