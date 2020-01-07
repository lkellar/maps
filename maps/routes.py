"""
Define routes.
"""
from datetime import datetime, timedelta
from flask import render_template, jsonify
from maps import app
from maps.models import Call

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch/<days>')
def fetch_days(days=1):
    days = float(days)

    # Get current date
    now = datetime.now(tz=app.config['TIMEZONE'])
    start = now - timedelta(days=days)

    data = Call.query.filter(Call.timestamp.between(start, now)).all()

    # Convert all the call objects to dict
    return jsonify([i.serialize for i in data])
