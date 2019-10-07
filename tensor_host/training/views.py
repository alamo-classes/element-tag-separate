from os import mkdir, getcwd, path
import subprocess
from shutil import copytree
from time import sleep

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from blocks.views import update_block_count
from training.models import *


class Train(View):
    """ View for /training/ """
    def get(self, request):
        blocks = BlockCatalog.objects.all()
        update_block_count(blocks)
        training_flag = blocks.filter(training_valid=True).count() >= 2
        networks = NeuralNets.objects.all()
        networks = check_networks(networks)
        return render(request, 'training/training.html', {'training_flag': training_flag, "networks": networks})

    @staticmethod
    def post(request):
        """ Delete a neural network """
        network_id = request.POST.get("network_id")
        NeuralNets.objects.get(id=network_id).delete()
        return HttpResponseRedirect('/training')


class TrainingForm(View):
    """ View for /training/training_form/ """
    @staticmethod
    def get(request):
        form = NeuralNetsForm()
        blocks = BlockCatalog.objects.filter(training_valid=True)
        return render(request, 'training/training_form.html', {'form': form, 'blocks': blocks})

    @staticmethod
    def post(request):
        form = NeuralNetsForm(request.POST)
        if form.is_valid():
            network = form.save()
            train_network(network)
            return HttpResponseRedirect('/training/')
        else:
            blocks = BlockCatalog.objects.filter(training_valid=True)
            return render(request, 'training/training_form.html', {'form': form, 'blocks': blocks})


def train_network(network):
    """
    Start a demonised thread to train the network based on the form. Once the training is done, update the network
    entry to reflect that the network is trained and ready to sort parts.
    """
    # Create a new directory for the network nested in the artifacts directory
    network_dir = path.join(getcwd(), "artifacts", "networks", network.name)
    network_dataset_dir = path.join(network_dir, "dataset")

    # Copy image directories of affected blocks to the new dataset directory
    for block in network.blocks.all():
        block_src = path.join(getcwd(), "artifacts", "dataset", str(block.part_number))
        copytree(block_src, path.join(network_dataset_dir, str(block.part_number)))

    mkdir(path.join(network_dir, "trained_model"))
    # mkdir(path.join(network_dir, "summaries"))
    image_dir = "dataset/"
    bottleneck_dir = "bottleneck/"
    training_steps = 500
    output_graph = "trained_model/retrained_graph.pb"
    output_labels = "trained_model/retrained_lables.txt"
    exe_path = path.join(getcwd(), "venv/bin/python")
    py_path = path.join(getcwd(), "training/train.py")
    command = [exe_path, py_path, "--image_dir={}".format(image_dir), "--bottleneck_dir={}".format(bottleneck_dir),
               "--how_many_training_steps={}".format(str(training_steps)), "--output_graph={}".format(output_graph),
               "--output_labels={}".format(output_labels), "--summaries_dir=summaries"]
    with open(path.join(network_dir, "training_log.txt"), "w") as out, \
            open(path.join(network_dir, "error_log.txt"), "w") as err:
        subprocess.Popen(command, cwd=network_dir, stdout=out, stderr=err)


def check_networks(networks):
    """ Check if the *.pb file has been generated for each defined neural networks. """
    for network in networks:
        if path.isfile(path.join(getcwd(), "artifacts/networks", network.name, "trained_model/retrained_graph.pb")):
            network.training_status = True
            network.save()
    return networks
