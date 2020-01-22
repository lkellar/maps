from datetime import datetime
import requests
import pytz

from maps import db
from maps.models import Call, CallQuery
from maps.scraper.geocoder import geocode_lookup
from maps.scraper.base import convert_naive_utc


SPRINGDALE_TZ = pytz.timezone('America/Chicago')


def geocode_calls(calls):
    addresses = [call.address for call in calls]
    address_to_geocode = geocode_lookup(addresses)

    for call in calls:
        # Lookup the coordinates for the address from our response
        result = address_to_geocode[call.address]
        lat, lon = result['coord']

        call.lat = lat
        call.lon = lon
        call.city = result['city']

    return calls


def scrape_to_db():
    """
    Function to scrape calls from Springdale source and insert them into the DB

    Springdale's response objects have the following schema:
        [
            %m/%d %H:%M:%S,
            CALL_TYPE,
            ADDRESS,
            DISPOSITION (which I guess is status)
        ]
    """

    # Interesting thing about springdale. It's a .txt extension, but it's in JSON format
    # Also, regardless of parameters, only the past 24 hours are shown.
    response_json = requests.get('https://ww2.springdalear.gov/web_includes/dispatch_logs.txt').json()

    new_calls = []
    for item in response_json['demo']:
        month_day, call_type, address, disposition = item
        if address:
            timestamp = generate_timestamp(month_day)
            call = Call(timestamp=timestamp, address=address, city='Springdale',
                        call_type=call_type, notes=disposition)
            existing_call = CallQuery.get_existing_springdale(call)

            # If call already exists
            if existing_call:
                # Update notes field on existing call
                existing_call.notes = disposition
            else:
                # Else, create new call
                new_calls.append(call)

    # Commit updates to calls
    db.session.commit()

    if new_calls:
        # Add lat/lon to calls using the geocoder
        new_calls = geocode_calls(new_calls)

        for call in new_calls:
            db.session.merge(call)

        # Commit new calls
        db.session.commit()


def generate_timestamp(month_day: str) -> datetime:
    """
    Take datetime info (provided as %m/%d) and create a timestamp out of it
    :param month_day: string following format "%m/%d"
    :return: utc datetime object
    """

    month, day = month_day.split('/')
    # Since springdale doesn't come w/ year, we provide our own
    year = datetime.now(SPRINGDALE_TZ).year

    # If it's January, 2020, and we have results from December, they were technically in 2019
    # So, we have to set it that way by subtracting a year
    if datetime.now().month == 1 and month == '12':
        year -= 1

    # Create a naive timestamp with the year
    timestamp = datetime.strptime(f'{year}/{month}/{day}', '%Y/%m/%d %H:%M:%S')

    # Then convert to UTC
    return convert_naive_utc(timestamp, SPRINGDALE_TZ)
