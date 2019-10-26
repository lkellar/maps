from flask import render_template, flash, redirect, url_for, request, jsonify
from maps import app, db
from maps.models import Call
from datetime import datetime, timedelta


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch/<days>')
def fetch_days(days=1):
    days = float(days)

    # get current date
    now = datetime.now(tz=app.config['TIMEZONE'])
    start = now - timedelta(days=days)

    data = Call.query.filter(Call.timestamp.between(start, now)).all()

    # convert all the call objects to dict
    return jsonify([i.serialize for i in data])
