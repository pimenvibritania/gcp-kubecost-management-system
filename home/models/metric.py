from django.db import models
from ..utils.enumerate import EnvironmentType
from .services import Services

class Metric(models.Model):
    class Meta:
        db_table = "metrics"

    service = models.ForeignKey(
            Services,
            on_delete=models.PROTECT,
            blank=False
        )

    environment = models.CharField(max_length=12, choices=EnvironmentType.choices())
    date = models.DateField(blank=False)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    total_cost = models.FloatField()

    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = False)
    updated_at = models.DateTimeField(auto_now = False, blank = False)
  
