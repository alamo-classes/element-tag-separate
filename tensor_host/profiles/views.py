from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views import View
from profiles.models import ProfileCatalog, ProfileForm
from training.models import NeuralNets


class Profile(View):
    """ View for /profile/ """
    @staticmethod
    def get(request):
        profiles = ProfileCatalog.objects.all()
        networks = NeuralNets.objects.filter(training_status=True)
        return render(request, 'profiles/profile.html', {'profiles': profiles, 'networks': networks})

    def post(self, request):
        pass


class ProfileCreateForm(View):
    """ View for /profile/form/ """
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
