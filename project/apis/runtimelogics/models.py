from flask_restx import Model, fields

logic_text_model = Model(
    "LogicText",
    {
        "logictext": fields.String(
            required=True, description="Logic text", example="logictext"
        ),
    },
)

regex_code_model = Model(
    "RegexCode",
    {
        "regex_code": fields.String(
            required=True, description="regex code", example="regex code"
        ),
    },
)

status_model = Model(
    "Status",
    {
        "status": fields.String(required=True, description="Status", example="status"),
    },
)

logic_text_and_regex_code_model = Model(
    "LogicTextAndRegexCode",
    {
        "logictext": fields.String(
            required=True, description="Logic text", example="logictext"
        ),
        "regex_code": fields.String(
            required=True, description="regex code", example="regex code"
        ),
    },
)
