from django.shortcuts import render

# Create your views here.
from django.views import View

from blocks.models import BlockCatalog


class Capture(View):
    @staticmethod
    def get(request):
        blocks = BlockCatalog.objects.all()
        return render(request, 'capture/capture.html', {'blocks': blocks})
