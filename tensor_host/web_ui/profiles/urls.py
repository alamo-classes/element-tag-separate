from django.urls import path

from tensor_host.web_ui.profiles.views import Profile

urlpatterns = [
    path('', Profile.as_view())
]
