from django.shortcuts import render
from django.views import View


class Monitor(View):
    def get(self, request):
        return render(request, 'monitor/monitor.html', {})

    def post(self, request):
        pass
