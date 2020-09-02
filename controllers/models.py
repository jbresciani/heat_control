from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.

class Thermostats(models.Model):
    name = models.CharField(max_length=30, unique=True)
    group = models.CharField(max_length=128)
    description = models.TextField()
    url = models.CharField(max_length=128)
    current_temp = models.IntegerField(default=14)
    requested_temp = models.IntegerField(default=14)

from django.forms import ModelForm

class ThermostateForm(ModelForm):
    class Meta:
        model = Thermostats
        exclude = ('current_temp','requested_temp')


def get_all_thermostats():
    return Thermostats.objects.all()


def add_thermostat(request):
    thermostatForm = ThermostateForm(request.POST)
    if thermostatForm.is_valid():
        print(f"----- Adding {thermostatForm.data['name']}")
        newThermostat = Thermostats(
            name=thermostatForm.cleaned_data['name'],
            group=thermostatForm.cleaned_data['group'],
            description=thermostatForm.cleaned_data['description'],
            url=thermostatForm.cleaned_data['url'])
        newThermostat.save()
    return thermostatForm.errors


def edit_thermostat(request):
    thermostatForm = ThermostateForm(request.POST)
    if thermostatForm.is_valid():
        print(f"----- Updating {thermostatForm.data['id']}")
        thermostat = get_object_or_404(Thermostats, id=thermostatForm.data['id'])
        thermostat.name = request.POST['name']
        thermostat.group = request.POST['group']
        thermostat.description = request.POST['description']
        thermostat.url = request.POST['url']
        thermostat.save(update_fields=['name', 'group', 'description', 'url'])
    return thermostatForm.errors


def delete_thermostat(id):
    print(f'----- Deleting {id}')
    Thermostats.objects.filter(id=id).delete()


def update_thermostat_temp(request):
    thermostat = get_object_or_404(Thermostats, id=request.POST['id'])
    thermostat.requested_temp = request.POST['requested_temp']
    thermostat.save(update_fields=["requested_temp"])
