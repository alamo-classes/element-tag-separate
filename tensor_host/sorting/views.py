from django.shortcuts import render
from django.views import View


class Sorting(View):
    """ View for /sorting/ page"""
    def get(self, request):
        return render(request, 'monitor/monitor.html', {})

    def post(self, request):
        pass
