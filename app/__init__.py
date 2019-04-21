# noqa: E402
import os

from configparser import ConfigParser
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from twilio.rest import Client

app = Flask(__name__)

# ENV Vars
try:
    ENV = os.environ['ENV']
    ENV in ('STAGING', 'PRODUCTION')
except Exception as e:
    raise EnvironmentError(
        f'Environmental variable "ENV" not found or unrecognized value {e}'
    )

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config.from_pyfile(basedir + '/config.py')

parser = ConfigParser()
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
tc = Client(
    app.config.get('TWILIO_ACCOUNT_SID'),
    app.config.get('TWILIO_ACCOUNT_AUTH')
)

from . import routes  # noqa
