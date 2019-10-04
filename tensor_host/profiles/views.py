import json

from django.shortcuts import render

from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blocks.models import BlockCatalog
from profiles.models import ProfileCatalog, ProfileForm
from training.models import NeuralNets


class Profile(View):
    @staticmethod
    def get(request):
        profiles = ProfileCatalog.objects.all()
        networks = NeuralNets.objects.all()
        return render(request, 'profiles/profile.html', {'profiles': profiles, 'networks': networks})

    def post(self, request):
        pass


class ProfileCreateForm(View):
    @staticmethod
    def get(request, network_id):
        form = ProfileForm()
        blocks = BlockCatalog.objects.all()
        return render(request, 'profiles/profile_form.html', {'form': form, 'blocks': blocks})

    @staticmethod
    def post(request):
        pass


class ProfileEditForm(View):
    @staticmethod
    def get(request, profile_id):
        profile = ProfileCatalog.objects.get(id=profile_id)
        form = ProfileForm(instance=profile)
        return render(request, 'profiles/profile_form.html', {'form': form, 'profile': profile})

    @staticmethod
    def post(request, profile_id):
        pass

@api_view(['GET'])
def detection_sorting_alert(request):
    msg = json.dumps({'status': status.HTTP_200_OK})
    return Response(msg)
