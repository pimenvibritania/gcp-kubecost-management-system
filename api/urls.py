from django.urls import path, include

from .views import (
    TodoListApiView,
    TodoDetailApiView
)

from .controllers.bigquery_controller import BigQueryController

urlpatterns = [
    path('', TodoListApiView.as_view()),
    path('<int:todo_id>/', TodoDetailApiView.as_view()),
    path('get-project', BigQueryController.as_view()),
    path('get-tf', BigQueryController.get_tf),
    path('sync-index', BigQueryController.post_index_weight),
]
