import logging
from flask import abort, Blueprint, render_template, redirect, request, send_from_directory, flash
from uuid import uuid1
from .extensions import db
from .models import Thermostats
from .form_schemas import create_thermostat_schema


control = Blueprint('control', __name__)

logger = logging.getLogger(__name__)


def find_thermostat_by_name(name):
    """ find a thermostat entry by name """
    if db.session.query(db.session.query(Thermostats).filter_by(name=name.lower()).exists()).scalar():
        logger.error("Thermostat already exists")
        return True
    return False


def create_thermostat_data(request):
    if request.form['action'] == 'new':
        thermostat_id = str(uuid1())
    else:
        thermostat_id = request.form['id']
    return {
        'id': thermostat_id,
        'name': request.form['name'],
        'group': request.form.get('group', request.form['name']),
        'description': request.form['description'],
        'url': request.form['url'],
    }


def add_thermostat(thermostat_data):
    """
    Save the changes to the database
    """
    db.session.add(Thermostats(**thermostat_data))
    db.session.commit()
    print(f"-------- Added Thermostat {thermostat_data['name']}")


@control.route('/set_temp', methods=['POST'])
def set_temp():
    thermostat = {}
    thermostat['name'] = request.form['thermostat_name']
    thermostat['requested_temp'] = request.form['requested_temp']
    logger.info(f"recieved request for {thermostat}")


@control.route('/favicon.ico')
def favicon():
    return send_from_directory(
        directory='./static/images/',
        filename='favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@control.route('/temperature_control', methods=['POST', 'GET'])
def temperature_control():
    warning_message = {}
    if request.method == 'POST':
        errors = None
        if request.form['action'] == "delete":
            Thermostats.delete(request.form['id'])
        if request.form['action'] == "edit":
            Thermostats.update(create_thermostat_data(request))
        if request.form['action'] == "change_temp":
            Thermostats.update({'id': request.form['id'], 'requested_temp': request.form['requested_temp']})
        if request.form['action'] == "new":
            thermostat_data = create_thermostat_data(request)
            errors = create_thermostat_schema.validate(thermostat_data)
            if errors:
                warning_message = errors
            elif find_thermostat_by_name(request.form['name']):
                warning_message = {'name': f"The name {thermostat_data['name']} is already in use"}
            else:
                add_thermostat(thermostat_data)

    thermostats = Thermostats.get_thermostats()
    groups = set(thermostat['group'] for thermostat in thermostats)
    return render_template('temperature_control.html', thermostats=thermostats, groups=groups, warning_message=warning_message)


@control.route('/')
def home():
    return redirect("/temperature_control", code=302)
