from django.db import models
from .enumerate import ProjectType, EnvironmentType, ServiceType
# Create your models here.

class TechFamily(models.Model):
  class Meta:
      db_table = "tech_family"
  
  name = models.CharField(max_length = 100)
  pic = models.CharField(max_length = 100)
  pic_email = models.EmailField(max_length=25)
  slug = models.CharField(max_length=25)
  project = models.CharField(
      max_length=30,
      choices=ProjectType.choices()
    )
  created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = False)
  updated_at = models.DateTimeField(auto_now = True, blank = False)

  def __str__(self):
    return self.name

class IndexWeight(models.Model):
    class Meta:
        db_table = "index_weight"

    tech_family = models.ForeignKey(
        TechFamily,
        on_delete=models.PROTECT,
        blank=False
    )

    value = models.FloatField()

    environment = models.CharField(max_length=12, choices=EnvironmentType.choices())
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = False)

    def __str__(self):
        return self.value

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

class Metric(models.Model):
    class Meta:
        db_table = "metric"

    service = models.ForeignKey(
            Service,
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
  
