from django.urls import path

from tensor_host.training.views import Train

urlpatterns = [
    path('', Train.as_view()),
]