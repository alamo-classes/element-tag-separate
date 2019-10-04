from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from blocks.views import update_block_count
from training.models import *


class Train(View):
    @staticmethod
    def get(request):
        blocks = BlockCatalog.objects.all()
        update_block_count(blocks)
        training_flag = blocks.filter(training_valid=True).count() >= 2
        networks = NeuralNets.objects.all()
        return render(request, 'training/training.html', {'training_flag': training_flag, "networks": networks})


class TrainingForm(View):
    @staticmethod
    def get(request):
        form = NeuralNetsForm()
        blocks = BlockCatalog.objects.filter(training_valid=True)
        return render(request, 'training/training_form.html', {'form': form, 'blocks': blocks})

    @staticmethod
    def post(request):
        form = NeuralNetsForm(request.POST)
        # TODO: Need to add validation that at least two different blocks were chosen
        if form.is_valid():
            # TODO: Run training
            print("Valid form")
            form.save()
            return HttpResponseRedirect('/training/')
        else:
            print(form.errors)
            blocks = BlockCatalog.objects.filter(training_valid=True)
            return render(request, 'training/training_form.html', {'form': form, 'blocks': blocks})
