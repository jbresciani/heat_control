import requests
from apscheduler.schedulers.background import BackgroundScheduler
from heating.models import Thermostats, get_all_thermostats


class RemoteThermostat(object):
    def __init__(self, thermostat):
        self.thermostat = thermostat
    
    def update_temp(self):
        response = requests.get(self.thermostat.url)
        response.raise_for_status()
        self.thermostat.current_temp = response.json()['current_temp']
        self.thermostat.save(update_fields=["current_temp"])


def update_current_temp_values():
    for thermostat in get_all_thermostats():
        RemoteThermostat(thermostat).update_temp()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_current_temp_values, 'interval', minutes=1)
    scheduler.start()