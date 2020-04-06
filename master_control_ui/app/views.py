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


def add_thermostat(request):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    thermostat = {
        'id': str(uuid1()),
        'name': request.form['name'].lower(),
        'group': request.form['group'],
        'description': request.form['description'],
        'url': request.form['url']
    }
    db.session.add(Thermostats(**thermostat))
    db.session.commit()
    logger.info(f"Added Thermostat {thermostat['name']}")


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
        print(f'-------------------------------- {request.form} --------------------------------')
        if request.form['action'] == "delete":
            print('delete thermostat')
        if request.form['action'] == "edit":
            print('edit thermostat')
            Thermostats.update_row({
                'id': request.form['id'],
                'name': request.form['name'],
                'description': request.form['description'],
                'url': request.form['url'],
                })
        if request.form['action'] == "change_temp":
            Thermostats.update_row({'id': request.form['id'], 'requested_temp': request.form['requested_temp']})
        if request.form['action'] == "new":
            errors = create_thermostat_schema.validate(request.form)
            if errors:
                warning_message = errors
            elif find_thermostat_by_name(request.form['name']):
                warning_message = {'name': 'That thermostat name is already in use'}
            else:
                add_thermostat(request)

    thermostats = Thermostats.get_thermostats()
    groups = set(thermostat['group'] for thermostat in thermostats)
    return render_template('temperature_control.html', thermostats=thermostats, groups=groups, warning_message=warning_message)


@control.route('/')
def home():
    return redirect("/temperature_control", code=302)
