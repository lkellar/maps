from datetime import datetime
from maps import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.timestamp()
    # return value.strftime("%Y-%m-%dT%H:%M:%SZ")


class Call(db.Model):
    __tablename__ = 'calls'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    city = db.Column(db.String)
    call_type = db.Column(db.String)
    address = db.Column(db.String)

    __table_args__ = (db.UniqueConstraint('timestamp', 'lat', 'lon', 'call_type', 'city', 'address'),)

    def __repr__(self):
        return '<Call {} {},{} {}>'.format(self.call_type, self.lat, self.lon, self.timestamp)

    def __init__(self, row):
        self.timestamp = datetime.strptime(row['DispatchTime'] + ' ' + row['DispatchTime2'], '%m-%d-%Y %H:%M:%S')
        self.lat = float(row['lat'])
        self.lon = float(row['lon'])
        self.city = row['City']
        self.call_type = row['CallType']
        self.address = row['Address']

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {'timestamp': dump_datetime(self.timestamp),
                'lat': self.lat,
                'lon': self.lon,
                'city': self.city,
                'call_type': self.call_type,
                'address': self.address}


class CallQuery:
    @staticmethod
    def get_call_exists(call):
        exists = db.session.query(Call.id).filter_by(
            timestamp=call.timestamp, lat=call.lat, lon=call.lon, city=call.city, call_type=call.call_type,
            address=call.address
        ).scalar() is not None
        return exists

