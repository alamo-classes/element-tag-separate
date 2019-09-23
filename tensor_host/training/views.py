from django.shortcuts import render
from django.views import View


class Train(View):
    def get(self, request):
        return render(request, 'training/training.html', {})