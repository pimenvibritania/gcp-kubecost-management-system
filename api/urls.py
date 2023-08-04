from django.urls import path, include

from .views.bigquery_views import BigQueryViews

urlpatterns = [
    path('get-project', BigQueryController.as_view()),
    path('get-tf', BigQueryController.get_tf),
    path('sync-index', BigQueryController.post_index_weight),
]
