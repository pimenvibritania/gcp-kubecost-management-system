from django.urls import path, include
from .views.bigquery_views import BigQueryViews
# from .views.report_views import index, async_view, sync_view, test_async
from .views.kubecost.cluster_views import KubecostClusterViews
from .views.service_views import ServiceViews
from .views.kubecost.namespace_views import KubecostNamespaceViews
from .views.kubecost.deployments_views import KubecostDeploymentViews
from .views.kubecost.namespace_map_views import KubecostNamespaceMapViews
from .views.kubecost.insert_data_views import KubecostInsertDataViews

urlpatterns = [
    path('get-project', BigQueryViews.as_view()),
    path('get-tf', BigQueryViews.get_tf),
    path('sync-index', BigQueryViews.post_index_weight),
    # path("test", test_async),
    # path("", index)
    path('services', ServiceViews.as_view()),
    path('kubecost/clusters', KubecostClusterViews.as_view()),
    path('kubecost/namespaces', KubecostNamespaceViews.as_view()),
    path('kubecost/deployments', KubecostDeploymentViews.as_view()),
    path('kubecost/namespace-map', KubecostNamespaceMapViews.as_view()),
    path('kubecost/insert-data', KubecostInsertDataViews.as_view()),
]
