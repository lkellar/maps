"""
Define SQLAlchemy models for the database.
"""
#pylint: disable=no-member, too-many-arguments

from datetime import datetime
from maps import db


def dump_datetime(value):
    """Deserialize datetime object into iso format for JSON processing."""
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')


class Call(db.Model):
    __tablename__ = 'calls'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    city = db.Column(db.String)
    call_type = db.Column(db.String)
    address = db.Column(db.String)
    # Okay, so some cities (like S-dale of course), have extra info, that is still imporatnt, but
    # not every city will have it. So this is a general notes field, that is intended to be
    # returned if available, and ignored if not.
    notes = db.Column(db.String, nullable=True)

    __table_args__ = (
        # Two calls are duplicates if they share the same values for these parameters
        # I changed the lat lon in favor of address because
        # W/ springdale, If I want to see if a call is in the db, so I don't have to do a Bing
        # lookup, I can't use coords to compare because the new call won't have any yet.
        # This should still keep out duplicates.
        db.UniqueConstraint('timestamp', 'address', 'call_type'),
    )

    def __init__(self, timestamp: datetime, lat: float, lon: float, city: str, call_type: str,
                 address: str, notes: str = None):
        '''
        Default Initializer

        timestamp (datetime): A UTC timestamp of when the call took place
        lat (float): The latitude of the event
        lon (float): The longitude of the event
        call_type (str): The type of call
        city (str): The city the event occurs in
        address (str): The address of the event
        '''
        self.timestamp = timestamp
        self.lat = lat
        self.lon = lon
        self.call_type = call_type
        self.city = city
        self.address = address
        self.notes = notes

    def __repr__(self):
        """Return string representation of call"""
        return '<Call {} {},{} {}>'.format(self.call_type, self.lat, self.lon, self.timestamp)

    @property
    def serialize(self):
        """Return object data in easily serializable format; for converting to JSON"""
        return {'timestamp': dump_datetime(self.timestamp),
                'lat': self.lat,
                'lon': self.lon,
                'city': self.city,
                'call_type': self.call_type,
                'address': self.address,
                'notes': self.notes}


class CallQuery:
    """Custom queries for calls table"""
    @staticmethod
    def get_existing_id(call):
        """Return the id of the call if an equivalent call already exists in the database"""
        # For the change from address to lat lon, see the comment up above on the __table_args__
        return db.session.query(Call.id).filter_by(
            timestamp=call.timestamp, address=call.address, call_type=call.call_type
        ).scalar()

    @staticmethod
    # Pls don't type set call, BECAUSE, springdale makes a mock call object w/ not everything to
    # check for duplicates before bing maps lookups
    def get_existing_call(call):
        '''Return a call if it exists in the db already'''
        return db.session.query(Call).filter_by(
            timestamp=call.timestamp, address=call.address, call_type=call.call_type
        ).scalar()
