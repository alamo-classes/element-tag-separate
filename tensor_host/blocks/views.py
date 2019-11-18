from os import path, listdir, getcwd

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from blocks.models import BlockCatalog, BlockForm


class Blocks(View):
    """ View for /blocks/ """
    @staticmethod
    def get(request):
        blocks = BlockCatalog.objects.all()
        update_block_count(blocks)
        return render(request, 'blocks/blocks.html', {'blocks': blocks})


class BlockProfile(View):
    """ View for /blocks/form/ """
    @staticmethod
    def get(request):
        form = BlockForm()
        return render(request, 'blocks/block_form.html', {'form': form})

    @staticmethod
    def post(request):
        form = BlockForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/blocks')
        else:
            return render(request, 'blocks/block_form.html', {'form': form, 'errors': form.errors})


class BlockProfileEdit(View):
    """ View for /blocks/form/ """
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
            return render(request, 'blocks/block_form.html', {'form': form, 'errors': form.errors})


def update_block_count(blocks):
    """
    Update the photo count of the blocks based on what is in the artifacts directory.
    If the number of photos is over the the required threshold,
    :param blocks: Query set of blocks to have their photo count updated
    """
    # TODO: image count should be minimum 200?
    for block in blocks:
        block_artifact_directory = path.join(getcwd(), "artifacts/dataset/", str(block.part_number))
        if path.exists(block_artifact_directory):
            block.photo_count = len([file for file in listdir(block_artifact_directory)])
            if block.photo_count > 1:
                block.training_valid = True
            block.save()
