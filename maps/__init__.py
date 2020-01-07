#pylint: disable=wrong-import-position
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

from config import Config, basedir

# Set up server configuration
app = Flask(__name__, static_folder='static', static_url_path='/static',
            template_folder='templates')
app.config.from_object(Config)
db = SQLAlchemy(app)


# If a sentry URL exists, enable sentry error reporting
SENTRY_DSN = os.environ.get('MAPS_SENTRY_DSN')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration(), SqlalchemyIntegration()]
    )

# Set routes and define models
from maps import routes, models
