""" Model containing all block information """
from django import forms
from django.db import models


class BlockCatalog(models.Model):
    """
    part_number = Catalog number of the part in question
    description = Physical (usually size/shape) description of the part
    category = Part category (i.e. Brick, Plate, etc.)
    photo_count = Number of photos related to this part in the 'artifacts/dataset' directory
    training_valid = Flag which is set once the photo count is high enough to be used to train a network
    """
    part_number = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    category = models.CharField(max_length=128, blank=True, null=True)
    color_wording = models.CharField(max_length=128)

    photo_count = models.IntegerField(default=0)
    training_valid = models.BooleanField(default=False)

    def __str__(self):
        """ If string is requested from the model object, return the part number """
        return str(self.part_number)

    class Meta:
        verbose_name_plural = "Block Catalog"


class BlockForm(forms.ModelForm):
    """ Django form template based off of the 'Block Catalog' model """
    class Meta:
        model = BlockCatalog
        verbose_name = "Catalog of All Blocks"
        exclude = ['photo_count', 'training_valid']
