from os import path
from datetime import datetime, timedelta
import sqlite3

from flask import Flask, g, jsonify, request, render_template

from maps.config import *


app = Flask(__name__, static_folder='../static', static_url_path='/static',
            template_folder='../templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = '../data.sqlite3'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch')
def fetch_days():
    # get a db instance from get_db
    cursor = get_db().cursor()

    if request.args.get('days'):
        days = int(request.args.get('days'))
    else:
        days = 7

    # get current date
    now = datetime.now(tz=TIMEZONE)
    start = now - timedelta(days=days)

    data = cursor.execute('SELECT * FROM calls WHERE datetime BETWEEN ? and ?', (start, now)).fetchall()

    # convert all the rows to a dict
    data = [dict(i) for i in data]
    return jsonify(data)


def get_db():
    db = getattr(g, '_database', None)
    if not db:
        db = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = sqlite3.Row
        g._database = db

    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db:
        db.close()


if __name__ == "__main__":
    app.run()
