from django.urls import path

from tensor_host.web_ui.training.views import Train

urlpatterns = [
    path('', Train.as_view()),
]