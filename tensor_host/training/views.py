from django.shortcuts import render
from django.views import View

from blocks.models import BlockCatalog


class Train(View):
    def get(self, request):
        blocks = BlockCatalog.objects.all()
        return render(request, 'training/training.html', {'blocks': blocks})
