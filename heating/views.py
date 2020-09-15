from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import get_all_thermostats, ThermostateForm, add_thermostat, delete_thermostat, edit_thermostat, update_thermostat_temp


def home_view(requests):
    return redirect('thermostats_control/', permanent=False)


def get_thermostat_context():
    thermostats = get_all_thermostats()
    context = {
        "full_thermostat_form": ThermostateForm(),
        "groups": {thermostat.group for thermostat in thermostats},
        "thermostats": thermostats
    }
    return context


class thermostatsControlView(View):
    def get(self, request):
        return render(request, 'thermostats_control.html', get_thermostat_context())

    def post(self, request):
        form_errors = None
        if request.POST['action'] == 'new':
            form_errors = add_thermostat(request)
        if request.POST['action'] == 'edit':
            form_errors = edit_thermostat(request)
        if request.POST['action'] == 'delete':
            delete_thermostat(request.POST['id'])
        if request.POST['action'] == 'update':
            update_thermostat_temp(request)
        context = get_thermostat_context()
        context['form_errors'] = form_errors
        return render(request, 'thermostats_control.html', context)
