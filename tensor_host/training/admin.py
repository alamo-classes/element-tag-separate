""" Add the training model to the admin section """
from django.contrib import admin
from training.models import NeuralNets

admin.site.register(NeuralNets)
