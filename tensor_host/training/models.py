import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django import forms

from blocks.models import BlockCatalog


class NeuralNets(models.Model):
    """
    id: Primary Key (Unique)
    name: Name of the Neural Network (Unique)
    description: Description of the Neural Network
    blocks: Blocks used to train the Neural Network
    training_status: Boolean field which signifies whether the network has been trained
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    blocks = models.ManyToManyField(BlockCatalog)
    training_status = models.BooleanField(default=False)

    def __str__(self):
        """ If a string is requested from the model object, return the name of the network """
        return self.name

    class Meta:
        verbose_name_plural = "Neural Networks"


class NeuralNetsForm(forms.ModelForm):
    """ Form to define new neural networks """
    def clean_blocks(self):
        """ Validation Check. Check if at least 2 blocks are selected to train the network. """
        blocks = self.cleaned_data['blocks']
        if blocks.count() < 2:
            raise ValidationError("At least 2 blocks must be chosen to train the network")
        return blocks

    class Meta:
        model = NeuralNets
        verbose_name = "Catalog of all Neural Networks"
        exclude = ['block_count', 'training_status', 'training_time_start', 'training_time_total']
