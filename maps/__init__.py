# pylint: disable=wrong-import-position
"""
File for initializing and running flask application.
"""

import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

import config

# Need this for instance
current_dir = os.path.dirname(os.path.realpath(__file__))

# Set up server configuration
app = Flask(__name__, static_folder='static', static_url_path='/static',
            template_folder='templates', instance_relative_config=True)
app.config.from_object(config)
# Doing it manually, because apache can mess with working dir
app.config.from_pyfile(os.path.join('../', current_dir, 'instance', 'config.py'))

# If a sentry URL exists, enable sentry error reporting
if app.config.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[FlaskIntegration(), SqlalchemyIntegration()]
    )

# Initialize Flask SQLAlchemy extension
db = SQLAlchemy(app)


# Set routes and define models
from maps import routes, models
