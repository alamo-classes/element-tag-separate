from django.urls import path

from capture.views import Capture

urlpatterns = [
    path('', Capture.as_view(), name='capture'),
]