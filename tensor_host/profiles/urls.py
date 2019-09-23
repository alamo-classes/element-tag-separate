from django.urls import path

from tensor_host.profiles.views import Profile

urlpatterns = [
    path('', Profile.as_view())
]
