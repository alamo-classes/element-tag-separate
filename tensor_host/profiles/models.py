from django import forms
from django.db import models

from blocks.models import BlockCatalog


class ProfileTags(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.CharField(max_length=128)


class ProfileCatalog(models.Model):
    """ Table containing all defined profiles and their relative neural network information """
    name = models.CharField(max_length=128)
    tags = models.ManyToManyField(ProfileTags)
    blocks = models.ManyToManyField(BlockCatalog)


class ProfileForm(forms.ModelForm):
    """ Form to construct a new profile """
    class Meta:
        model = ProfileCatalog
        verbose_name = "Catalog of All Profiles"
        exclude = []
