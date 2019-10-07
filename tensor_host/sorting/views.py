from django.shortcuts import render
from django.views import View

from profiles.models import ProfileCatalog


class Sorting(View):
    """ View for /sorting/ page"""
    @staticmethod
    def get(request):
        profiles = ProfileCatalog.objects.all()
        return render(request, 'monitor/monitor.html', {'profiles': profiles})
