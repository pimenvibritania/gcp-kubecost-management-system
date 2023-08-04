from django.urls import path, include

from .views.bigquery_views import BigQueryViews

urlpatterns = [
    path('get-project', BigQueryViews.as_view()),
    path('get-tf', BigQueryViews.get_tf),
]
