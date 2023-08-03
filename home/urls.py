from django.urls import path, include

from . import views
from .controllers.gcp import gcp_controller
from .controllers.kubecost import kubecost_controller


urlpatterns = [
    path('', views.index, name='index'),
    path('metrics', gcp_controller.index, name='index_metrics'),
    path('kubecost-test', kubecost_controller.index, name='kubecost-test'),

]
