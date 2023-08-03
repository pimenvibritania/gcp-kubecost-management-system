from babel.numbers import format_currency

class Conversion:
  @classmethod
  def idr_format(cls, value):
    return format_currency(value, 'IDR', locale='id_ID')
