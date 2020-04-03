from marshmallow import Schema, fields, validate


class CreateThermostatSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(max=128))
    location = fields.String(required=False, validate=validate.Length(max=128))
    group = fields.String(required=False, validate=validate.Length(max=128))
    description = fields.String(required=False, validate=validate.Length(max=256))
    url = fields.String(required=True, validate=validate.URL())


create_thermostat_schema = CreateThermostatSchema()
