import logging
import time
from .thermostats import update_thermostats
from .extensions import scheduler

logger = logging.getLogger(__name__)

@scheduler.task('interval', id='update_thermostats', minutes=5, misfire_grace_time=30)
def update_servers():
    app = scheduler.app
    with app.app_context():
        update_thermostats()
