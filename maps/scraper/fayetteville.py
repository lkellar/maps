from datetime import datetime
import requests
import pytz

from maps.models import Call, CallQuery
from maps import db
from .base import *


FAYETTEVILLE_TZ = pytz.timezone('America/Chicago')
URL = 'https://maps.fayetteville-ar.gov/DispatchLogs/json/getIncidents.cshtml/{}/{}'


def format_date(dt: datetime):
    return dt.strftime("%Y-%m-%d")


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
        # If coordinates are not specified, we don't want to insert the call
        if (call.lat, call.lon) != (-361, -361):
            existing_call = CallQuery.get_existing_fayetteville(call)
            if existing_call:
                # If call already exists, update the existing call
                call.id = existing_call.id
            db.session.merge(call)
    db.session.commit()


def create_call(row: dict) -> Call:
    """ Take raw data from the scraper and puts it into a Call object """

    # Create a naive timestamp from the date (DispatchTime) and time (DispatchTime2)
    timestamp = datetime.strptime(row['DispatchTime'] + '' + row['DispatchTime2'],
                                  '%m-%d-%Y%H:%M:%S')
    # Then convert to UTC
    timestamp = convert_naive_utc(timestamp, FAYETTEVILLE_TZ)

    lat = float(row['lat'])
    lon = float(row['lon'])

    return Call(timestamp=timestamp, lat=lat, lon=lon,
                city=row['City'], call_type=row['CallType'], address=row['Address'])
