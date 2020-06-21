"""
Define SQLAlchemy models for the database.
"""
# pylint: disable=no-member, too-many-arguments

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
    # General notes field if available
    notes = db.Column(db.String, nullable=True)

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
    """ Custom queries for calls table """

    @staticmethod
    def get_existing_with_latlon(call):
        """ Return a call if it exists in the db already, using lat/lon to verify same location """
        return db.session.query(Call).filter_by(
            timestamp=call.timestamp, lat=call.lat, lon=call.lon, call_type=call.call_type,
        ).first()

    @staticmethod
    def get_existing_with_address(call):
        """ Return a call if it exists in the db already, using address to verify same location """
        # Using first instead of scalar, as first 
        return db.session.query(Call).filter_by(
            timestamp=call.timestamp, address=call.address, call_type=call.call_type).first()
