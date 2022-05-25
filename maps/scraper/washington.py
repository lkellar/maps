from datetime import datetime

from bs4 import BeautifulSoup
import requests
import pytz

from maps import db
from maps.models import Call, CallQuery
from maps.util import convert_naive_to_db

from .geocoder.exceptions import BingStallError, BingTimeoutError
from .geocoder import geocode_lookup_city

WASHINGTON_TZ = pytz.timezone('America/Chicago')


def geocode_calls(calls: [Call]):
    addresses_cities = [{'address': call.address, 'city': call.city} for call in calls]
    address_to_geocode = geocode_lookup_city(addresses_cities)

    for call in calls:
        # Lookup the coordinates for the address from our response
        result = address_to_geocode[call.address]
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

    # Washington data source is an HTML response, containing table rows.
    # The rows contain properties of calls, in the form of tds which alternate key, value, key, value.
    # Some rows contain only an hr (horizontal rule), acting as a separator between rows that, together, make up a call.
    response = requests.get('https://www.so.washington.ar.us/res/callsforservice.aspx').text

    # Use bs4 for html parsing
    soup = BeautifulSoup(response, 'html.parser')

    # Find all table rows, except first one (which is empty)
    rows = soup.find_all('tr')[1:]
    td_groups = []  # List containing groups of tds (each group representing a call)
    new_group = []  # Latest group of tds (representing a call)

    for tr in rows:
        # If row contains a horizontal rule separator, latest group is finished
        if tr.find('hr'):
            # Append finished group
            td_groups.append(new_group)
            # Prepare for next group
            new_group = []
        else:
            # Else, append new tds to latest group
            new_group += tr.find_all('td')

    new_calls = []
    for tds in td_groups:
        call_props = {}

        # This trick will raise a StopIteration exception if there are an odd number of items
        # But if there are an odd number of items, we have a bigger problem
        iterator = iter(tds)
        try:
            for td in iterator:
                key, val = td.text.replace(':', ''), next(iterator).text
                call_props[key] = val
        except StopIteration as e:
            print(tds)
            raise e

        address = call_props.get('Location', None)
        if address:
            address = address.replace('  ', ' ').strip()
            timestamp = generate_timestamp(call_props['Date'], call_props['Time'])
            city = call_props['City'].strip()

            # call and case number, both optional, note attributes
            notes = []
            call_number = call_props['Call Number']
            if call_number:
                notes.append(f'Call Number: {call_number}')
            case_number = call_props['Case Number']
            if case_number:
                notes.append(f'Case Number: {case_number}')
            notes = '\n'.join(notes)

            call = Call(timestamp=timestamp, address=address, call_type=call_props['Type'], notes=notes, city=city)

            existing_call = CallQuery.get_existing_with_address(call)
            if existing_call:
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

    # Convert to database timezone and return
    return convert_naive_to_db(timestamp, WASHINGTON_TZ)
