from .models import Thermostats


def get_current_tempurature(thermostat):
    ''' get the current tempurature reading from a thermostat 
    Inputs:
        thermostat (dict): a dictionary defining the thermostat name and url for reading
    
    Returns:
        the current temp in celcius
    '''
    mock_values = {
        'default': 18,
        'living room': 15,
        'kitchen': 15,
        'bed1': 13,
        'bed2': 18,
        'master bed': 13,
        'office': 13
    }
    return mock_values.get(thermostat['name'], 8)


def update_thermostats():
    for thermostat in Thermostats.get_thermostats():
        thermostat['current_temp'] = get_current_tempurature(thermostat)
        Thermostats.update(thermostat)
