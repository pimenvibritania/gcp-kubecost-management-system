from rest_framework import status

class UnprocessableEntityException():
  def __init__(self, message):
    self.message = message
    self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

class BadRequestException():
  def __init__(self, message):
    self.message = message
    self.status_code = status.HTTP_400_BAD_REQUEST