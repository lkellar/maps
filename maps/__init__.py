"""
File for initializing and running flask application.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Set up server configuration
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

if not app.debug and not app.testing:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    handler = RotatingFileHandler('logs/maps.log', maxBytes=10240, backupCount=1)
    app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Crime Map startup')


# Set routes and define models
from maps import routes, models