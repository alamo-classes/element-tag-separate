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
        if not ElementSettings.objects.first():
            return HttpResponseRedirect("/settings/")
        return render(request, 'capture/capture.html', {'blocks': blocks})


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
        pass
