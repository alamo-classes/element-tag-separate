from django.urls import path, include
from rest_framework import routers

from tensor_host.profiles.views import Profile, ProfileCreateForm, ProfileEditForm, detection_training_alert, \
    detection_sorting_alert

urlpatterns = [
    path('/', Profile.as_view(), name="profile"),
    path('/form/', ProfileCreateForm.as_view(), name="profile_create"),
    path('/form/<int:profile_id>/', ProfileEditForm.as_view(), name="profile_edit"),
    path('/detection_training/', detection_training_alert, name="detection_training"),
    path('/detection_sorting/', detection_sorting_alert)
]
