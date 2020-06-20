"""
Define application-wide configuration.
"""

import os
import pytz
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = False


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# DATABASE TIMEZONE. All datetimes are converted to this before being entered in the database
TIMEZONE = pytz.timezone("UTC")
