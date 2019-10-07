""" Model containing all profile information """
from django import forms
from django.db import models

from blocks.models import BlockCatalog
from training.models import NeuralNets


class ProfileCatalog(models.Model):
    """ Table containing all defined profiles and their relative neural network information """
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    network = models.ForeignKey(NeuralNets, on_delete=models.CASCADE, blank=True, null=True)
    bin_1 = models.ManyToManyField(BlockCatalog, blank=True, related_name="bin_1_blocks")
    bin_2 = models.ManyToManyField(BlockCatalog, blank=True, related_name="bin_2_blocks")
    bin_3 = models.ManyToManyField(BlockCatalog, blank=True, related_name="bin_3_blocks")
    bin_4 = models.ManyToManyField(BlockCatalog, blank=True, related_name="bin_4_blocks")
    bin_5 = models.ManyToManyField(BlockCatalog, blank=True, related_name="bin_5_blocks")
    bin_6 = models.ManyToManyField(BlockCatalog, blank=True, related_name="bin_6_blocks")


class ProfileForm(forms.ModelForm):
    """ Form to construct a new profile """
    class Meta:
        model = ProfileCatalog
        verbose_name = "Catalog of All Profiles"
        exclude = ['network']
