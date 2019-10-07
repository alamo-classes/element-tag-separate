""" URL Resolution for sorting application """
from django.urls import path
from sorting.views import Sorting

urlpatterns = [
    path('', Sorting.as_view(), name='sorting'),
]
