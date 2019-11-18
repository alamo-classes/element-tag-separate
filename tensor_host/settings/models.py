""" Model containing all settings information """
from django.db import models
from django import forms


class ElementSettings(models.Model):
    """ Model to store the setting for the Element system. """
    rpi_id_addr1 = models.GenericIPAddressField()
    rpi_id_addr2 = models.GenericIPAddressField()
    tolerance = models.FloatField()


class ElementSettingForm(forms.ModelForm):
    """ Form to construct the new setting """
    class Meta:
        model = ElementSettings
        verbose_name = "Form for Project-wide Setting"
        exclude = []
