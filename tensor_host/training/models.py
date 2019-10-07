import uuid

from django.db import models
from django import forms
from django.utils.datetime_safe import datetime

from blocks.models import BlockCatalog


class NeuralNets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    blocks = models.ManyToManyField(BlockCatalog)
    training_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Neural Networks"


class NeuralNetsForm(forms.ModelForm):
    class Meta:
        model = NeuralNets
        verbose_name = "Catalog of all Neural Networks"
        exclude = ['block_count', 'training_status', 'training_time_start', 'training_time_total']
