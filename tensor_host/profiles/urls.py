from django.urls import path
from profiles.views import Profile, ProfileCreateForm, ProfileEditForm, detection_sorting_alert

urlpatterns = [
    path('', Profile.as_view(), name="profile"),
    path('form/', ProfileCreateForm.as_view(), name="profile_create"),
    path('form/<int:profile_id>/', ProfileEditForm.as_view(), name="profile_edit"),
    path('detection_sorting/', detection_sorting_alert, name="detection_sorting")
]
