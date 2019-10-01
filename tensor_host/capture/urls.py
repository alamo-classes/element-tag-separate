from django.urls import path

from capture.views import Capture, detection_training_alert

urlpatterns = [
    path('', Capture.as_view(), name='capture'),
    path('detection_training/<str:label>/', detection_training_alert, name="detection_training"),
]