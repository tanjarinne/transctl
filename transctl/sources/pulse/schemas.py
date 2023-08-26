from marshmallow import Schema, fields


class Result(fields.Decimal):
  _excluded_tokens = {
    "↑",
    "↓",
    "<",
    ">",
  }

  def _remove_tokens(self, value):
    return " ".join([v for v in value.split() if v not in self._excluded_tokens])

  def _validated(self, value):
    value = self._remove_tokens(value)
    return super()._validated(value)


class SIResult(Result):
  pass


class ConventionalResult(Result):
  pass


class PulseSchema(Schema):
  def columns(self):
    columns = list(self._declared_fields.keys())
    return columns


class BiochemistrySchema(PulseSchema):
  test                   = fields.Str(required=True)
  test_chinese           = fields.Str(required=True)
  si_result              = SIResult(required=True)
  si_unit                = fields.Str(required=True)
  si_reference           = fields.Str(required=True)
  conventional_result    = ConventionalResult()
  conventional_unit      = fields.Str()
  conventional_reference = fields.Str()


class EndocrinologySchema(PulseSchema):
  test                   = fields.Str(required=True)
  test_chinese           = fields.Str(required=True)
  si_result              = SIResult(required=True)
  si_unit                = fields.Str(required=True)
  si_reference           = fields.Str(required=True)
  conventional_result    = ConventionalResult()
  conventional_unit      = fields.Str()
  conventional_reference = fields.Str()


class SerologySchema(PulseSchema):
  test         = fields.Str(required=True)
  test_chinese = fields.Str(required=True)
  result       = fields.Str(required=True)
  unit         = fields.Str(required=True, allow_none=True)
  reference    = fields.Str(required=True)


class HaematologySchema(PulseSchema):
  test         = fields.Str(required=True)
  test_chinese = fields.Str()
  si_result    = SIResult()
  si_unit      = fields.Str(required=True)
  si_reference = fields.Str(required=True)


schemas = {
  'BIOCHEMISTRY': BiochemistrySchema,
  'ENDOCRINOLOGY': EndocrinologySchema,
  'SEROLOGY': SerologySchema,
  'HAEMATOLOGY': HaematologySchema,
}
