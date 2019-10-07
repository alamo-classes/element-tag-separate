""" URL Resolution for profile application """
from django.urls import path
from profiles.views import Profile, ProfileCreateForm, detection_sorting_alert

urlpatterns = [
    path('', Profile.as_view(), name="profile"),
    path('form/<uuid:network_id>/', ProfileCreateForm.as_view(), name="profile_create"),
    path('detection_sorting/', detection_sorting_alert, name="detection_sorting")
]
