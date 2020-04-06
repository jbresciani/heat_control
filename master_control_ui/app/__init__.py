import logging
import os
from .config import Config, configure_logging
from .extensions import db, ma, scheduler
from .schedules import update_servers
from .thermostats import update_thermostats
from .models import Thermostats
from .views import add_thermostat
from flask import Flask
from flask.logging import default_handler

logger = logging.getLogger(__name__)

class MockRecord(object):
    def __init__(self):
        self.form = {
            'name': 'default',
            'group': 'default',
            'description': 'default for dev purposes',
            'url': 'https://127.0.0.1:8080/'
        }


def setup_schedules(app):
    update_thermostats()


def create_app():
    """Initialize the core application."""
    configure_logging()
    app = Flask(__name__)
    app.config.from_object(Config)

    scheduler.api_enabled = True
    scheduler.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        app.logger.removeHandler(default_handler)
        db.create_all()
        db.session.commit()
        if app.config['ENV'] == 'development':
            default = MockRecord()
            if db.session.query(db.session.query(Thermostats).filter_by(name=default.form['name']).exists()).scalar():
                print('default record exists')
            else:
                add_thermostat(default)
        else:
            print('********************** not adding default thermostat **********************')

        scheduler.start()
        update_thermostats()

        # Include our Routes
        from . import views

        # Register Blueprints
        app.register_blueprint(views.control)

        return app
