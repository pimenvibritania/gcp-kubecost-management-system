from django.urls import path, include
from .views.bigquery_views import BigQueryViews
from .views.report_views import test_async
from .views.service_views import ServiceViews
from .views.report_views import test_async
from .views.kubecost_view import KubecostClusterViews
from .views.service_views import ServiceViews
from .views.kubecost_view import KubecostNamespaceViews
from .views.kubecost_view import KubecostDeploymentViews
from .views.kubecost_view import KubecostNamespaceMapViews
from .views.kubecost_view import KubecostInsertDataViews

urlpatterns = [
    path('get-project', BigQueryViews.as_view()),
    path('get-tf', BigQueryViews.get_tf),
    path('create-index', BigQueryViews.post_index_weight),
    path("test", test_async),
    path('services', ServiceViews.as_view()),
    path('kubecost/clusters', KubecostClusterViews.as_view()),
    path('kubecost/namespaces', KubecostNamespaceViews.as_view()),
    path('kubecost/deployments', KubecostDeploymentViews.as_view()),
    path('kubecost/namespace-map', KubecostNamespaceMapViews.as_view()),
    path('kubecost/insert-data', KubecostInsertDataViews.as_view()),
]