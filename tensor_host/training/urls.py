from django.urls import path

from training.views import Train

urlpatterns = [
    path('', Train.as_view(), name='training'),
]