from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from settings.models import ElementSettingForm, ElementSettings


def index(request):
    return render(request, 'settings/index.html')


class SettingForm(View):
    @staticmethod
    def get(request):
        setting_instance = ElementSettings.objects.first()
        form = ElementSettingForm()
        if setting_instance:
            form = ElementSettingForm(instance=setting_instance)
        return render(request, 'settings/setting_form.html', {'form': form, 'setting_instance': setting_instance})

    @staticmethod
    def post(request):
        setting_instance = ElementSettings.objects.first()
        form = ElementSettingForm(request.POST, instance=setting_instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, 'settings/setting_form.html', {'form': form, 'setting_instance': setting_instance})
