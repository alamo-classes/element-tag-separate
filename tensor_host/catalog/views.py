from django.shortcuts import render
from django.views import View


class Catalog(View):
    def get(self, request):
        return render(request, 'catalog/catalog.html', {})

    def post(self):
        pass
