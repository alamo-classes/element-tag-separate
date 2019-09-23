from django.urls import path
from tensor_host.monitor.views import Monitor

urlpatterns = [
    path('', Monitor.as_view()),
]
