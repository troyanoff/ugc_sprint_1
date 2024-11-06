from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import INCLUDE, Schema, fields
from marshmallow.validate import OneOf

DOCS_FILENAME = "docs/docs.yaml"


class InputActionSchema(Schema):
    action = fields.String(
        description="Action",
        required=True,
        validate=OneOf(["click", "view", "quality_change", "video_progress", "query"]),
    )


class LogActionSchema(Schema):
    id = fields.String(description="Action's id ", required=True)
    user_id = fields.String(description="User's id", required=True)
    event_dt = fields.DateTime(description="Datetime of action", required=True)

    class Meta:
        unknown = INCLUDE


def get_apispec(app):
    spec = APISpec(
        title="ugc-sprint-1",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        security=[{"BearerAuth": []}],
    )
    spec.components.security_scheme(
        "BearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    spec.components.schema("InputAction", schema=InputActionSchema)
    spec.components.schema("LogAction", schema=LogActionSchema)

    load_docstrings(spec, app)
    write_yaml_file(spec)

    return spec


def load_docstrings(spec, app):
    with app.test_request_context():
        for fn_name in app.view_functions:
            if fn_name == "static":
                continue
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)


def write_yaml_file(spec: APISpec):
    with open(DOCS_FILENAME, "w") as file:
        file.write(spec.to_yaml())
