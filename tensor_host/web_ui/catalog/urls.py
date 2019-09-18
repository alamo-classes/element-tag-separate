from django.urls import path

from tensor_host.web_ui.catalog.views import Catalog

urlpatterns = [
    path('', Catalog.as_view()),
]