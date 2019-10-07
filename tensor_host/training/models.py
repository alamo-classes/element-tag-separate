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
    block_count = models.IntegerField(default=0)
    training_status = models.BooleanField(default=False)
    training_time_start = models.DateTimeField()
    training_time_total = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # If initial save set the initial time that training began.
        # If consequent save set the total time that training ran.
        if self.training_time_start:
            self.training_time_total = datetime.now() - self.training_time_start
        else:
            self.training_time_start = datetime.now()
        super(NeuralNets, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Neural Networks"


class NeuralNetsForm(forms.ModelForm):
    class Meta:
        model = NeuralNets
        verbose_name = "Catalog of all Neural Networks"
        exclude = ['block_count', 'training_status', 'training_time_start', 'training_time_total']
