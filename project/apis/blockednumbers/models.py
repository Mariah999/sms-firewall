from flask_restx import Model, fields

blockednumber_model = Model(
    "Blockednumber",
    {
        "senderId": fields.String(
            required=True, description="Sender Id", example="senderId"
        ),
        "destStartsWith": fields.List(
            fields.String,
            required=False,
            description="Destination Starts With",
            example=["88017"]
        ),
    },
)
