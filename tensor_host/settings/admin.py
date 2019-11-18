""" Add the Settings's model to the admin section """
from django.contrib import admin
from settings.models import ElementSettings

admin.site.register(ElementSettings)
