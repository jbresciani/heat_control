import logging
import logging.config
import os


logger = logging.getLogger(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir + '/sqlite')


class Config(object):
    ENV = os.environ.get('ENVRONMENT', 'development')
    DEBUG = True if ENV == 'development' else False

    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'kjhsdkjfhgoawiueghfkajbcnvlaehuwrfkljbn')
    SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost.localdomain:8080')

    # Configure the SQLAlchemy part of the app instance
    # echo sql calls to console
    SQLALCHEMY_ECHO = True if ENV == 'development' else False
    # turning off the SQLAlchemy event system, which is on by default.
    # The event system generates events useful in event-driven programs but adds significant overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(db_path, 'controls.db')
    print(SQLALCHEMY_DATABASE_URI)

def configure_logging():
    ''' configure logging '''
    # disable requests warnings about certificate verification
    from requests.packages.urllib3 import disable_warnings
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    disable_warnings(InsecureRequestWarning)
    log_level = os.environ.get('FLASK_LOG_LEVEL', 'INFO')
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s]: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'threads': {
                'format': '%(asctime)s [%(levelname)s](%(thread)d): %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'precise': {
                'format': '%(asctime)s [%(levelname)s] %(name)s(%(thread)d): %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'precise'
            }
        },
        'loggers': {
            '': {
                'handlers': ['wsgi'],
                'level': log_level,
                'propagate': True,
            }
        }
    })
