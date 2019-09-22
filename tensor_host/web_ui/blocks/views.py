from django.shortcuts import render
from django.views import View


class Blocks(View):
    def get(self, request):
        return render(request, 'blocks/blocks.html', {})
