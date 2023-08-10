from datetime import datetime, timedelta
from dateutil.parser import parse
from django.http import JsonResponse
from ..utils.exception import UnprocessableEntityException, BadRequestException
class Date:
  def __init__(self):
    self.status_code = 200
  @classmethod
  def get_date_range(cls, input_date):
    est_date = datetime.strptime(input_date, "%Y-%m-%d")
    current_week = est_date - timedelta(days=6)
    current_week_to = current_week - timedelta(days=1)
    previous_week = current_week - timedelta(days=7)

    f_current_week = current_week.strftime("%Y-%m-%d")
    f_current_week_to = current_week_to.strftime("%Y-%m-%d")
    f_previous_week = previous_week.strftime("%Y-%m-%d")

    current_week_from = f_current_week
    current_week_to = input_date
    previous_week_from = f_previous_week
    previous_week_to = f_current_week_to

    return current_week_from, current_week_to, previous_week_from, previous_week_to

  @classmethod
  def validate(cls, value):
    try:
        if value is None:
          return BadRequestException("date query parameter is required")
        parsed_date = parse(value)
        if parsed_date.strftime('%Y-%m-%d') != value:
          return UnprocessableEntityException("Date format must be 'Y-m-d' (e.g., '2023-08-07')")
        return cls()
    except ValueError:
      return UnprocessableEntityException("Invalid date format. Must be 'Y-m-d' (e.g., '2023-08-07')")
    
