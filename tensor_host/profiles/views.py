import json

from django.shortcuts import render

from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from profiles.models import ProfileCatalog, ProfileForm


class Profile(View):
    @staticmethod
    def get(request):
        profiles = ProfileCatalog.objects.all()
        return render(request, 'profile/profile.html', {'profiles': profiles})

    def post(self, request):
        pass


class ProfileCreateForm(View):
    @staticmethod
    def get(request):
        form = ProfileForm()
        return render(request, 'profile/profile_form.html', {'form': form})

    @staticmethod
    def post(request):
        pass


class ProfileEditForm(View):
    @staticmethod
    def get(request, profile_id):
        profile = ProfileCatalog.objects.get(id=profile_id)
        form = ProfileForm(instance=profile)
        return render(request, 'profile/profile_form.html', {'form': form, 'profile': profile})

    @staticmethod
    def post(request, profile_id):
        pass


@api_view(['GET'])
def detection_training_alert(request):
    print("Got a REST get request")
    msg = json.dumps({'status': status.HTTP_200_OK})
    return Response(msg)


@api_view(['GET'])
def detection_sorting_alert(request):
    print("Got a Rest get sorting request")
    msg = json.dumps({'status': status.HTTP_200_OK})
    return Response(msg)
