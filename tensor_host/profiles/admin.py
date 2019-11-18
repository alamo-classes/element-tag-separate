""" Add the Profile's model to the admin section """
from django.contrib import admin
from profiles.models import ProfileCatalog

admin.site.register(ProfileCatalog)
