from flask_restx import Model, fields

rule_model = Model(
    'Rule', 
    {
        'rule_type': fields.String(
            required=True, description='Type of rule (block or pass)', enum=['block', 'pass']
        ),
        'category': fields.String(
            required=True, description='Category of the rule', enum=['length', 'sequence']
        ),
        'features': fields.Raw(
            required=True, description='Description of the rule (JSON format)'
        )
    }
)

update_rule_model = Model(
    'updateRule', 
    {
        'rule_type': fields.String(
            description='Type of rule (block or pass)', enum=['block', 'pass']
        ),
        'status': fields.Boolean(
            description='Status of SMS'
        )
    }
)