from datetime import datetime
import requests
import pytz

from maps.models import Call, CallQuery
from maps import db
from maps.util import convert_naive_to_db


FAYETTEVILLE_TZ = pytz.timezone('America/Chicago')
URL = 'https://maps.fayetteville-ar.gov/DispatchLogs/json/getIncidents.cshtml/{}/{}'


def format_date(dt: datetime):
    return dt.strftime("%Y-%m-%d")


def is_invalid(call):
    return (call.lat, call.lon) == (-361, -361) or call.address == "<UNKNOWN>" or call.city is None


def scrape_to_db(start: datetime, end: datetime):
    """
    Scrape Fayetteville calls and insert into the DB
    :param start: The datetime object at which to begin collection. Inclusive (Only date portion is used)
    :param end: The datetime object at which to end collection. Inclusive (Only date portion is used)
    """

    # Fetch the fayetteville url and substitute in start and end date
    url = URL.format(format_date(start), format_date(end))
    response_json = requests.get(url).json()

    for row in response_json:
        # Generate call object from json data
        call = create_call(row)
        # If coordinates or address or city are not specified, we don't want to insert the call
        if not is_invalid(call):
            # Check for existing call using lat/lon as location, rather than address, which may be unspecified?
            existing_call = CallQuery.get_existing_with_latlon(call)
            if existing_call:
                call.id = existing_call.id  # If call already exists, update the existing call
            db.session.merge(call)
    db.session.commit()


def create_call(row: dict) -> Call:
    """ Take raw data from the scraper and puts it into a Call object """

    # Create a naive timestamp from the date (DispatchTime) and time (DispatchTime2)
    timestamp = datetime.strptime(row['DispatchTime'] + '' + row['DispatchTime2'],
                                  '%m-%d-%Y%H:%M:%S')
    # Then convert to database timezone
    timestamp = convert_naive_to_db(timestamp, FAYETTEVILLE_TZ)

    lat = float(row['lat'])
    lon = float(row['lon'])

    return Call(timestamp=timestamp, lat=lat, lon=lon,
                city=row['City'], call_type=row['CallType'], address=row['Address'])
