"""
File for initializing and running flask application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Set up server configuration
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


# Start server
from maps import routes, models