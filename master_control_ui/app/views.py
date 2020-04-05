import logging
from flask import abort, Blueprint, render_template, redirect, request, send_from_directory, flash
from uuid import uuid1
from .extensions import db
from .models import Thermostats
from .form_schemas import create_thermostat_schema


control = Blueprint('control', __name__)

logger = logging.getLogger(__name__)


@control.route('/set_temp', methods=['POST'])
def set_temp():
    thermostat = {}
    thermostat['name'] = request.form['thermostat_name']
    thermostat['requested_temp'] = request.form['requested_temp']
    logger.info(f"recieved request for {thermostat}")

@control.route('/favicon.ico')
def favicon():
    return send_from_directory(
        directory='./static/',
        filename='favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@control.route('/temperature_control', methods=['POST', 'GET'])
def temperature_control():
    if request.method == 'POST':
        print(request.form)
        Thermostats.update_row(request.form)
    thermostats = Thermostats.get_thermostats()
    groups = set(thermostat['group'] for thermostat in thermostats)
    print(f"{groups}")
    return render_template('temperature_control.html', thermostats=thermostats, groups=groups)


def add_thermostat(request):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    thermostat = {
        'id': str(uuid1()),
        'name': request.form['name'].lower(),
        'location': request.form['location'],
        'group': request.form['group'],
        'description': request.form['description'],
        'url': request.form['url']
    }
    db.session.add(Thermostats(**thermostat))
    db.session.commit()
    logger.info(f"Added Thermostat {thermostat['name']}")


def find_thermostat_by_name(name):
    """ find a thermostat entry by name """
    if db.session.query(db.session.query(Thermostats).filter_by(name=name.lower()).exists()).scalar():
        logger.error("Thermostat already exists")
        return True
    return False


@control.route('/create_thermostat', methods=['GET', 'POST'])
def create_thermostat():
    """ Add a new thermostat """
    warning_message = {}
    if request.method == 'POST':
        errors = create_thermostat_schema.validate(request.form)
        if errors:
            warning_message = errors
        elif find_thermostat_by_name(request.form['name']):
            warning_message = {'name': 'That thermostat name is already in use'}
        else:
            add_thermostat(request)
            return redirect('/temperature_control')


    return render_template('create_thermostat.html', warning_message=warning_message)


@control.route('/change_temperature', methods=['POST'])
def change_temperature():
    """ Add a new thermostat """
    print(request)


@control.route('/')
def home():
    return redirect("/temperature_control", code=302)
