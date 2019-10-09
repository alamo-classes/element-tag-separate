""" URL Resolution for sorting application """
from django.urls import path
from sorting.views import Sorting, detection_sorting_alert

urlpatterns = [
    path('', Sorting.as_view(), name='sorting'),
    path('detection_sorting/<str:profile_id>/', detection_sorting_alert, name="detection_sorting")
]
