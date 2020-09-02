from django.db import models

# Create your models here.

class Thermostats(models.Model):
    name = models.CharField(max_length=30, unique=True)
    group = models.CharField(max_length=128)
    description = models.TextField()
    url = models.CharField(max_length=128)
    current_temp = models.IntegerField(default=14)
    requested_temp = models.IntegerField(default=14)

from django.forms import ModelForm

class newOrUpdateThermostateForm(ModelForm):
    class Meta:
        model = Thermostats
        exclude = ('current_temp','requested_temp')


def get_all_thermostats():
    return Thermostats.objects.all()


def addThermostat(request):
    thermostatForm = newOrUpdateThermostateForm(request.POST)
    if thermostatForm.is_valid():
        print(f"----- adding {thermostatForm.data['name']}")
        newThermostat = Thermostats(
            name=thermostatForm.cleaned_data['name'],
            group=thermostatForm.cleaned_data['group'],
            description=thermostatForm.cleaned_data['description'],
            url=thermostatForm.cleaned_data['url'])
        newThermostat.save()
    return thermostatForm.errors


def updateThermostat(request):
    thermostatForm = newOrUpdateThermostateForm(request.POST)
    if thermostatForm.is_valid():
        print(f"----- updating {thermostatForm.data['id']}")
        updateThermostat = Thermostats(
            id=thermostatForm.data['id'],
            name=thermostatForm.cleaned_data['name'],
            group=thermostatForm.cleaned_data['group'],
            description=thermostatForm.cleaned_data['description'],
            url=thermostatForm.cleaned_data['url'])
        updateThermostat.save()
    return thermostatForm.errors


def deleteThermostat(id):
    print(f'----- deleting {id}')
    Thermostats.objects.filter(id=id).delete()
