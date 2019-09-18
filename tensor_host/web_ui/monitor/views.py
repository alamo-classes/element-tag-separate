from django.shortcuts import render

# Create your views here.
from django.views import View


class Monitor(View):
    def get(self, request):
        return render(request, 'monitor.html', {'test': 'test'})

    def post(self, request):
        pass