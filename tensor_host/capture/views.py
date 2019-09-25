from django.shortcuts import render

# Create your views here.
from django.views import View


class Capture(View):
    def get(self, request):
        return render(request, 'capture/capture.html', {})
