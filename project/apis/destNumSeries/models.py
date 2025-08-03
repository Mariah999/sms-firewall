from flask_restx import Model, fields

dest_num_series_model = Model(
    "DestNumSeries",
    {
        "startsWith": fields.String(
            required=True, description="Destination Number startsWith", example="8801700"
        ),
    },
)