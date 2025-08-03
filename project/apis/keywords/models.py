from flask_restx import Model, fields

keyword_model = Model(
    "Keyword",
    {
        "name": fields.String(
            required=True, description="Keyword name", example="keyword"
        ),
    },
)
