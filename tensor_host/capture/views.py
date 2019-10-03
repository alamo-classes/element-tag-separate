import glob
import os
import io
import time
from urllib import request

from PIL import Image
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json

from blocks.models import BlockCatalog
from settings.models import ElementSettings


class Capture(View):
    @staticmethod
    def get(request):
        blocks = BlockCatalog.objects.all()
        settings = ElementSettings.objects.first()
        if not settings:
            return HttpResponseRedirect("/settings/")
        return render(request, 'capture/capture.html', {'blocks': blocks, 'settings': settings})

    @staticmethod
    def post(request):
        """
        Used by the Capture application to poll for an updated photo count.
        Send the last image of the part (if exists) to the client.
        """
        # TODO: Redo this to use a template insertion
        # part_id = request.POST.get("part_id")
        # if os.path.exists(os.path.join("../artifacts/", part_id)):
        #     file_list = glob.glob(os.path.join("../artifacts/", part_id, "*"))
        #     time_hack = []
        #     for part_file in file_list:
        #         time_hack.append(part_file.split("_")[1].split(".")[0])
        #     return HttpResponse(file(os.path.join("../artifacts/", "{}.jpg".format(max(time_hack)))))
        pass


@api_view(['GET'])
def detection_training_alert(request, label):
    """Raspberry Pi Rest request will send a message telling the server to take an image for training."""
    capture_image = CaptureLabeledImages(label)
    capture_image.capture_image()
    msg = json.dumps({'status': status.HTTP_200_OK})
    return Response(msg)


class CaptureLabeledImages:
    """Using the passed label, capture an image and place it in the appropriate directory"""
    def __init__(self, label):
        self.label = label

    def capture_image(self):
        """ Take a snapshot of the part and save it to the artifacts directory and database"""
        # Make directory (if needed) for part photos
        artifact_dir = os.path.join("../artifacts/", self.label)
        os.makedirs(artifact_dir, exist_ok=True)
        # Get settings file
        settings = ElementSettings.objects.first()
        # Increment the count of photos
        block = BlockCatalog.objects.get(part_number=self.label)
        block.photo_count = block.photo_count + 1
        # Take snapshot and save to a file
        file = io.BytesIO(request.urlopen("{}:5000/snapshot".format(settings.rpi_id_addr)).read())
        img = Image.open(file)
        # Use (label)_(UTC_time).jpg as file format
        img.save(os.path.join(artifact_dir, "dataset/", "{}_{}.jpg".format(self.label, str(int(time.time())))))
