"""Project-level URL Resolution"""
from django.contrib import admin
from django.urls import path, include

from settings.views import SettingForm, index

urlpatterns = [
    path('admin', admin.site.urls),
    path('', index, name='index'),
    path('blocks/', include('blocks.urls')),
    path('capture/', include('capture.urls')),
    path('training/', include('training.urls')),
    path('profiles/', include('profiles.urls')),
    path('sorting/', include('sorting.urls')),
    path('settings/', SettingForm.as_view(), name='settings')
]
