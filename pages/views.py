from django.shortcuts import render, redirect
from controllers.models import get_all_thermostats, newOrUpdateThermostateForm, addThermostat, updateThermostat, deleteThermostat
from django.http import HttpResponse
from django.views import View


def home_view(requests):
    return redirect('thermostats_control/', permanent=False)


def get_thermostats():
    return [{
        "id": "123451234",
        "name": "mockunit",
        "group": "mockgroup",
        "description": "mock",
        "url": "http://localhost:1234",
        "requested_temp": 10
    }]


def get_thermostat_context():
    thermostats = get_all_thermostats()
    context = {
        "full_thermostat_form": newOrUpdateThermostateForm(),
        "groups": {thermostat.group for thermostat in thermostats},
        "thermostats": thermostats
    }
    return context


class thermostatsControlView(View):
    def get(self, request):
        return render(request, 'thermostats_control.html', get_thermostat_context())

    def post(self, request):
        if request.POST['action'] == 'new':
            form_errors = addThermostat(request)
        if request.POST['action'] == 'edit':
            form_errors = updateThermostat(request)
        if request.POST['action'] == 'delete':
            form_errors = deleteThermostat(request.POST['id']) 
        context = get_thermostat_context()
        context['form_errors'] = form_errors
        return render(request, 'thermostats_control.html', context)
