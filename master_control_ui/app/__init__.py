import logging
import os
from .config import Config, configure_logging
from .extensions import db, ma, scheduler
from .schedules import update_servers
from .thermostats import update_thermostats
from .models import Thermostats
from flask import Flask
from flask.logging import default_handler

logger = logging.getLogger(__name__)


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
        scheduler.start()
        update_thermostats()

        # Include our Routes
        from . import views

        # Register Blueprints
        app.register_blueprint(views.control)

        return app
