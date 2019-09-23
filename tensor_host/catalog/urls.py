from django.urls import path

from tensor_host.catalog.views import Catalog

urlpatterns = [
    path('', Catalog.as_view()),
]