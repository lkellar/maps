"""
Define SQLAlchemy models for the database.
"""

import pytz
from datetime import datetime, timezone
from maps import db


def dump_datetime(value):
    """Deserialize datetime object into iso format for JSON processing."""
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')


def load_datetime(value):
    # naive datetime (no timezone attached)
    naive = datetime.strptime(value, '%m-%d-%Y %H:%M:%S')

    # attach proper timezone for the date (fayetteville.gov uses America/Chicago)
    pst = pytz.timezone('America/Chicago')
    dt = pst.localize(naive)

    # convert to UTC timezone
    dt = dt.astimezone(pytz.UTC)
    return dt


class Call(db.Model):
    __tablename__ = 'calls'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    city = db.Column(db.String)
    call_type = db.Column(db.String)
    address = db.Column(db.String)

    __table_args__ = (
        # Two calls are duplicates if they share the same values for these parameters
        db.UniqueConstraint('timestamp', 'lat', 'lon', 'call_type'),
    )

    def __repr__(self):
        """Return string representation of call"""
        return '<Call {} {},{} {}>'.format(self.call_type, self.lat, self.lon, self.timestamp)

    def __init__(self, row):
        """Construct a new call object based on data from scraper"""
        self.timestamp = load_datetime(row['DispatchTime'] + ' ' + row['DispatchTime2'])

        self.lat = float(row['lat'])
        self.lon = float(row['lon'])
        if (self.lat, self.lon) == (-361, -361):
            raise ValueError('Lat/lon must be specified.')

        self.city = row['City']
        self.call_type = row['CallType']
        self.address = row['Address']

    @property
    def serialize(self):
        """Return object data in easily serializable format; for converting to JSON"""
        return {'timestamp': dump_datetime(self.timestamp),
                'lat': self.lat,
                'lon': self.lon,
                'city': self.city,
                'call_type': self.call_type,
                'address': self.address}


class CallQuery:
    """Custom queries for calls table"""
    @staticmethod
    def get_existing_id(call):
        """Return the id of the call if an equivalent call already exists in the database"""
        return db.session.query(Call.id).filter_by(
            timestamp=call.timestamp, lat=call.lat, lon=call.lon, call_type=call.call_type
        ).scalar()

