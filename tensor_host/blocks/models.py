""" Model containing all block information """
from django import forms
from django.db import models


class BlockCatalog(models.Model):
    part_number = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    category = models.CharField(max_length=128, blank=True, null=True)
    color_wording = models.CharField(max_length=128)
    photo_count = models.IntegerField(default=0)


class BlockForm(forms.ModelForm):
    class Meta:
        model = BlockCatalog
        verbose_name = "Catalog of All Blocks"
        exclude = ['photo_count']
