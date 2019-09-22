from django.urls import path

from tensor_host.web_ui.blocks.views import Blocks

urlpatterns = [
    path('', Blocks.as_view())
]