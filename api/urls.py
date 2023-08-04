from django.urls import path, include

from .views.bigquery_views import BigQueryViews
from .views.report_views import index, async_view, sync_view, test_async

urlpatterns = [
    path('get-project', BigQueryViews.as_view()),
    path('get-tf', BigQueryViews.get_tf),
    path('sync-index', BigQueryViews.post_index_weight),
    path("test", test_async),
    path("", index)
]
