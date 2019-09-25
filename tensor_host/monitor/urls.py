from django.urls import path
from monitor.views import Monitor

urlpatterns = [
    path('', Monitor.as_view()),
]
