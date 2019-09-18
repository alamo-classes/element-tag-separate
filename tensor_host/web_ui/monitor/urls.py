from django.urls import path
from tensor_host.web_ui.monitor.views import Monitor

urlpatterns = [
    path('', Monitor.as_view()),
]
