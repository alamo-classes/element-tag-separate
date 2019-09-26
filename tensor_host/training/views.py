from django.shortcuts import render
from django.views import View

from blocks.models import BlockCatalog


class Train(View):
    @staticmethod
    def get(request):
        return render(request, 'training/training.html', {})


class TrainingForm(View):
    @staticmethod
    def get(request):
        return render(request, 'training/training_form.html', {})
