from django.db import models
from .enumerate import ProjectType, EnvironmentType
# Create your models here.

class TechFamily(models.Model):
  class Meta:
      db_table = "tech_family"
  
  name = models.CharField(max_length = 100)
  pic = models.CharField(max_length = 100)
  pic_email = models.EmailField(max_length=25)
  slug = models.CharField(max_length=25)
  project = models.CharField(
      max_length=5,
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