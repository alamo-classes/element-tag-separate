import os
from time import time
from urllib import request
import numpy as np
import cv2
from django.http import HttpResponseRedirect
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
        self.artifact_dir = os.path.join("artifacts/dataset/", self.label)
        self.file_path = os.path.join(self.artifact_dir, "{}_{}.jpg".format(self.label, int(time())))

    def capture_image(self):
        """ Take a snapshot of the part and save it to the artifacts directory and database"""
        # Make directory (if needed) for part photos
        os.makedirs(self.artifact_dir, exist_ok=True)

        # Get settings file
        settings = ElementSettings.objects.first()

        # Increment the count of photos
        block = BlockCatalog.objects.get(part_number=self.label)
        block.photo_count = block.photo_count + 1

        # Take snapshot and save to a file
        snapshot_request = request.urlopen("http://{}:5001/stream.mjpg".format(settings.rpi_id_addr))
        frame = snapshot_request.read(100000)

        # JPEG data if found between these two byte indexes
        a = frame.find(b"\xff\xd8")
        b = frame.find(b"\xff\xd9")
        if a != -1 and b != -1:
            jpg_bytes = frame[a:b+2]
            frame = frame[b+2]
            image = cv2.imdecode(np.fromstring(jpg_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imwrite(self.file_path, image)
