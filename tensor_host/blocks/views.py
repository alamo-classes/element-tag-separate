from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from blocks.models import BlockCatalog, BlockForm


class Blocks(View):
    @staticmethod
    def get(request):
        blocks = BlockCatalog.objects.all()
        return render(request, 'blocks/blocks.html', {'blocks': blocks})


class BlockProfile(View):
    @staticmethod
    def get(request):
        form = BlockForm()
        print("Get Request")
        return render(request, 'blocks/block_form.html', {'form': form})

    @staticmethod
    def post(request):
        form = BlockForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/blocks')
        else:
            return render(request, 'blocks/block_form.html', {'form': form})


class BlockProfileEdit(View):
    @staticmethod
    def get(request, part_number):
        part = BlockCatalog.objects.get(part_number=part_number)
        form = BlockForm(part)
        return render(request, 'blocks/block_form.html', {'form': form, 'part': part})

    @staticmethod
    def post(request, part_number):
        part = BlockCatalog.objects.get(part_number=part_number)
        form = BlockForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/blocks')
        else:
            print(form.errors)
            return render(request, 'blocks/block_form.html', {'form': form})
