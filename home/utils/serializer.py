from marshmallow import Schema, fields

class IndexWeightSerializer(Schema):
  value = fields.Float()
  environment = fields.Str()
  project = fields.Str()
  slug = fields.Str()