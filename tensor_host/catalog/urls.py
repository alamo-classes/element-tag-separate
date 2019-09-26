from django.urls import path

from catalog.views import Catalog

urlpatterns = [
    path('', Catalog.as_view(), name='catalog'),
]