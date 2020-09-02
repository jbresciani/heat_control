import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import get_object_or_404
from models import Thermostats, get_all_thermostats, get_thermostat


class RemoteThermostat(object):
    def __init__(self, id):
        self.id = id
        self.thermostat = get_thermostat(id)
    
    def update_temp(self):
        response = requests.get(self.thermostat.url)
        response.raise_for_status()
        thermostat = get_object_or_404(Thermostats, id=request.POST['id'])
        thermostat.current_temp = response.json()['current_temp']
        thermostat.save(update_fields=["current_temp"])


def update_current_temp_values():
    for thermostat in get_all_thermostats():
        print(thermostat.id)
        RemoteThermostat(thermostat.id).update_temp()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_current_temp_values, 'interval', minutes=1)
    scheduler.start()