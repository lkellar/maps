from datetime import datetime

from bs4 import BeautifulSoup
import requests
import pytz

from maps import db
from maps.models import Call, CallQuery
from maps.util import convert_naive_utc

from .geocoder.exceptions import BingStallError, BingTimeoutError
from .geocoder import geocode_lookup_city

WASHINGTON_TZ = pytz.timezone('America/Chicago')


def geocode_calls(calls: [Call]):
    addresses = list(({'address': call.address.strip(), 'city': call.city.strip()} for call in calls))
    address_to_geocode = geocode_lookup_city(addresses)

    for call in calls:
        # Lookup the coordinates for the address from our response
        result = address_to_geocode[call.address.strip()]
        call.lat = float(result['lat'])
        call.lon = float(result['lon'])
        call.city = result['city']

    return list(set(calls))


def scrape_to_db():
    """
    Function to scrape calls from Washington County's source and insert them into the DB

    Washington County's response objects have the following schema:
        CallNumber, CaseNumber, Date, Time, Assist, Location (Address), City
    """

    response = requests.get('https://www.so.washington.ar.us/res/callsforservice.aspx').text

    # No json, use BS4 for html parsing
    soup = BeautifulSoup(response, 'html.parser')

    # structure is a bunch of trs containing tds, one td for key, one td for value, then a tr containing
    # an hr to seperate calls
    # first row is empty
    rows = soup.find_all('tr')[1:]
    grouped_rows = []
    internal_row = []

    # basically a .split() where the param is trs with hr
    for row in rows:
        if row.find('hr'):
            grouped_rows.append(internal_row)
            internal_row = []
        else:
            internal_row.append(row)

    new_calls = []
    for trs in grouped_rows:
        # made of TRs with tds inside of them. We want to flatten to get all of the tds
        trs = [ele.find_all('td') for ele in trs]
        tds = []

        for tr in trs:
            tds += tr 
        
        # format is a td with a key, then a td with a value
        call_draft = {}

        # This trick will raise a StopIteration exception if there are an odd number of items
        # But if there are an odd number of items, we have a bigger problem
        it = iter(tds)
        try:
            for key in it:
                call_draft[key.text.replace(':', '')] = next(it).text
        except StopIteration as e:
            print(tds)
            raise e

        if address := call_draft.get('Location', None):
            address = address.replace('  ', ' ')
            timestamp = generate_timestamp(call_draft['Date'], call_draft['Time'])

            # call and case number, both optional, note attributes
            notes = []
            if call_number := call_draft['Call Number']:
                notes.append(f'Call Number: {call_number}')

            if case_number := call_draft['Case Number']:
                notes.append(f'Case Number: {case_number}')

            notes = '\n'.join(notes)

            # City is provided, but we aren't using it
            call = Call(timestamp=timestamp, address=address, call_type=call_draft['Type'], notes=notes, city=call_draft['City'])

            if existing_call := CallQuery.get_existing_with_address(call):
                existing_call.notes = notes
            else:
                new_calls.append(call)

    db.session.commit()

    if new_calls:
        try:
            # Add lat/lon and city to calls using the geo-coder
            new_calls = geocode_calls(new_calls)
        except (BingStallError, BingTimeoutError):
            # If bing is stalling (we have 3 pending jobs) or our job takes too long to complete,
            # just stop and come back later
            return

        for call in new_calls:
            db.session.merge(call)

        # Commit new calls
        db.session.commit()


def generate_timestamp(date: str, time: str) -> datetime:
    """
    Take a date and time and creat a timestamp out of it
    :param date: string following format %m/%d/%Y
    :param time: string following format HH:MM AM/PM
    :return utc datetime object
    """

    # Convert to datetime
    timestamp = datetime.strptime(f'{date} {time}', '%m/%d/%Y %H:%M %p')

    # Convert to UTC and return
    return convert_naive_utc(timestamp, WASHINGTON_TZ)
