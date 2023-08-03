from django.db import models
from ..utils.enumerate import ProjectType, ServiceType
from .tech_family import TechFamily

class Service(models.Model):
    class Meta:
        db_table = "service"

    name = models.CharField(max_length = 100)
    service_type = models.CharField(max_length=10, choices=ServiceType.choices())
    project = models.CharField(max_length=30, choices=ProjectType.choices())
    
    tech_family = models.ForeignKey(
        TechFamily,
        on_delete=models.PROTECT,
        blank=False
    )

    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = False)
    updated_at = models.DateTimeField(auto_now = False, blank = False)

    def __str__(self):
        return self.name
