import json
import operator
from os import mkdir, getcwd, path, makedirs
from time import time
from urllib.request import urlopen
import tensorflow as tf
import cv2
import numpy as np
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from profiles.models import ProfileCatalog
from settings.models import ElementSettings
from training.models import NeuralNets


class Sorting(View):
    """ View for /sorting/ page"""
    @staticmethod
    def get(request):
        profiles = ProfileCatalog.objects.all()
        settings = ElementSettings.objects.first()
        return render(request, 'sorting/sorting.html', {'profiles': profiles, 'settings': settings})


@api_view(['GET'])
def detection_sorting_alert(request, profile_id):
    # Get network & settings object from the database
    profile = ProfileCatalog.objects.get(id=profile_id)
    network = profile.network
    settings = ElementSettings.objects.first()

    # Create directory to store the snapshot
    network_dir = path.join(getcwd(), "artifacts/networks", network.name)
    makedirs(path.join(network_dir, 'testing'), exist_ok=True)
    test_file = path.join(network_dir, "testing/{}.jpg".format(str(int(time()))))

    snapshot_request = urlopen("http://{}:5001/stream.mjpg".format(settings.rpi_id_addr1))
    frame = snapshot_request.read(100000)

    a = frame.find(b"\xff\xd8")
    b = frame.find(b"\xff\xd9")
    if a != -1 and b != -1:
        jpg_bytes = frame[a:b + 2]
        image = cv2.imdecode(np.fromstring(jpg_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite(test_file, image)

    # Get headers for the trained network from generated labels tag in list format
    with open(path.join(network_dir, 'trained_model/retrained_labels.txt')) as labels_file:
        labels = labels_file.read()
    labels = labels.split('\n')[:-1]

    # Open trained network to categorize
    with tf.gfile.FastGFile(path.join(network_dir, "trained_model/retrained_graph.pb"), 'rb') as tensor_graph:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(tensor_graph.read())
        _ = tf.import_graph_def(graph_def, name='')

    # Run trained network to identify
    with tf.Session() as sess:
        # Read image data
        image_data = tf.gfile.FastGFile(test_file, 'rb').read()
        # Feed the image data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        # TODO: Clean this up after verification
        # records = []
        # row_dict = {}
        # head, tail = path.split(file)
        # row_dict['id'] = tail.split('.')[0]
        header_scores = dict()
        for node_id in top_k:
            header = labels[node_id]
            score = predictions[0][node_id]
            header_scores[header] = score
        print(header_scores.__str__())
    tensor_graph.close()

    # Get label based on top score
    top_score_label = max(header_scores.items(), key=operator.itemgetter(1))[0]

    # Get bin position based on label (if score is above percentage threshold)
    # TODO: Reenable after zoned in the cameras
    # if header_scores[top_score_label] >= settings.tolerance:
    if True:
        # Check each bin number for the part number label
        if profile.bin_1.all().filter(part_number=top_score_label).exists():
            position = 1
        elif profile.bin_2.all().filter(part_number=top_score_label).exists():
            position = 2
        elif profile.bin_3.all().filter(part_number=top_score_label).exists():
            position = 3
        elif profile.bin_4.all().filter(part_number=top_score_label).exists():
            position = 4
        elif profile.bin_5.all().filter(part_number=top_score_label).exists():
            position = 5
        elif profile.bin_6.all().filter(part_number=top_score_label).exists():
            position = 6
        else:
            position = 0
    else:
        # Set bin to 0 position if threshold is not met
        position = 0
    print("Position: {}".format(position))
    # Return status message with position
    return Response(position, status=status.HTTP_200_OK)


def send_logging(log_message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('broadcast', {'type': 'logging_event', 'data': log_message})
