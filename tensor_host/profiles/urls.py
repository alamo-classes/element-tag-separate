from django.urls import path

from tensor_host.profiles.views import Profile, ProfileCreateForm, ProfileEditForm

urlpatterns = [
    path('', Profile.as_view(), name="profile"),
    path('form/', ProfileCreateForm.as_view(), name="profile_create"),
    path('form/<int:profile_id>/', ProfileEditForm.as_view(), name="profile_edit"),
]
