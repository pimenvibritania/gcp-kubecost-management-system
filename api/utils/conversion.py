from babel.numbers import format_currency

class Conversion:
  @classmethod
  def unpack_idr(cls, value):
    numeric_string = value.replace("Rp", "").replace(".", "").replace(",", "")
    return float(numeric_string)

  @classmethod
  def idr_format(cls, value):
    return format_currency(value, 'IDR', locale='id_ID')

  @classmethod
  def usd_format(cls, value):
    return format_currency(value, 'USD', locale='en_US')
  
  @classmethod
  def convert_usd(cls, value, rate_idr):
    rate = cls.unpack_idr(rate_idr)
    return cls.usd_format(value/rate)
  