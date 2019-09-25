from django.shortcuts import render
from django.views import View

from settings.models import ElementSettingForm, ElementSettings


class SettingForm(View):
    @staticmethod
    def get(request):
        setting_instance = ElementSettings.objects.first()
        form = ElementSettingForm()
        if setting_instance:
            form = ElementSettingForm(instance=setting_instance)
        return render(request, 'settings/setting_form.html', {'form': form, 'setting_instance': setting_instance})
