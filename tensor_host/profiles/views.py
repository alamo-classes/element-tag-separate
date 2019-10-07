import json

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from profiles.models import ProfileCatalog, ProfileForm
from training.models import NeuralNets


class Profile(View):
    @staticmethod
    def get(request):
        profiles = ProfileCatalog.objects.all()
        networks = NeuralNets.objects.filter(training_status=True)
        return render(request, 'profiles/profile.html', {'profiles': profiles, 'networks': networks})

    def post(self, request):
        pass


class ProfileCreateForm(View):
    @staticmethod
    def get(request, network_id):
        form = ProfileForm()
        network = NeuralNets.objects.get(id=network_id)
        return render(request, 'profiles/profile_form.html', {'form': form, 'network': network})

    @staticmethod
    def post(request, network_id):
        form = ProfileForm(request.POST)
        network = NeuralNets.objects.get(id=network_id)
        if form.is_valid():
            profile = form.save()
            profile.network = network
            profile.save()
            return HttpResponseRedirect('/profiles/')
        else:
            return render(request, 'profiles/profile_form.html', {'form': form, 'network': network})


class ProfileEditForm(View):
    @staticmethod
    def get(request, profile_id):
        profile = ProfileCatalog.objects.get(id=profile_id)
        form = ProfileForm(instance=profile)
        return render(request, 'profiles/profile_form.html', {'form': form, 'profile': profile})

    @staticmethod
    def post(request, profile_id):
        pass


# TODO: This should move to sorting application
@api_view(['GET'])
def detection_sorting_alert(request):
    msg = json.dumps({'status': status.HTTP_200_OK})
    return Response(msg)
