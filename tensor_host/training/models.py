import uuid

from django.core.exceptions import ValidationError
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
    def clean_blocks(self):
        blocks = self.cleaned_data['blocks']
        if blocks.count() < 2:
            raise ValidationError("At least 2 blocks must be chosen to train the network")
        return blocks

    class Meta:
        model = NeuralNets
        verbose_name = "Catalog of all Neural Networks"
        exclude = ['block_count', 'training_status', 'training_time_start', 'training_time_total']
