from django.db import models
from ..utils.enumerate import EnvironmentType, ProjectType
from .services import Services
from .kubecost_clusters import KubecostClusters

class KubecostNamespaces(models.Model):
    class Meta:
        db_table = "kubecost_namespaces"
        constraints = [
            models.UniqueConstraint(
                fields=['namespace', 'cluster','date'],
                name='unique_namespace_cluster_date'
            )
        ]

    namespace = models.CharField(max_length=100)
    service = models.ForeignKey(Services, on_delete=models.PROTECT, null=True)
    date = models.DateField(blank=False)
    project = models.CharField(max_length=12, choices=ProjectType.choices())
    environment = models.CharField(max_length=12, choices=EnvironmentType.choices())
    cluster = models.ForeignKey(KubecostClusters, on_delete=models.PROTECT, blank=False, null=False)
    cpu_cost = models.FloatField()
    memory_cost = models.FloatField()
    pv_cost = models.FloatField()
    lb_cost = models.FloatField()
    network_cost = models.FloatField()
    total_cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=False)
  
    def __str__(self):
        return self.namespace


class KubecostNamespacesMap(models.Model):
    class Meta:
        db_table = "kubecost_namespace_map"
        constraints = [
            models.UniqueConstraint(
                fields=['namespace', 'project'],
                name='unique_namespace_project'
            )
        ]

    namespace = models.CharField(max_length=100)
    service = models.ForeignKey(Services, on_delete=models.PROTECT, blank=False)
    project = models.CharField(max_length=12, choices=ProjectType.choices())
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=False)
    updated_at = models.DateTimeField(auto_now=False, null=True)
  
    def __str__(self):
        return self.namespace

    @classmethod
    def get_all(cls):
        return cls.objects.all()
        
    @classmethod
    def get_namespaces_map(cls, project):
        return cls.objects.filter(project=project).values('service_id', 'namespace')
