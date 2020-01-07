from datetime import datetime
import requests

from maps.models import Call, CallQuery
from maps.scraper.base import BaseScraper

#pylint: disable=broad-except

def format_date(dt: datetime):
    return dt.strftime("%Y-%m-%d")

class FayettevilleScraper(BaseScraper):
    def __init__(self, db):
        self.url = 'https://maps.fayetteville-ar.gov/DispatchLogs/json/getIncidents.cshtml/{}/{}'
        self.db = db
        self.timezone = 'America/Chicago'

        # We gotta initilizate the Base Scraper!
        super().__init__(self.timezone)

    def scrape(self, start: datetime, end: datetime) -> [Call]:
        '''
        Scrape Fayetteville Calls

        start (datetime): The datetime object at which to begin collection. Inclusive;
            Only date portion is used
        end (datetime): The datetime object at whcih to end collection. Inclusive;
            Only date portion is used

        Returns: NOTHING. All calls are sent to DB
        '''

        # Fetch the fayetteville url and substitute in start and end date
        json_response = requests.get(self.url.format(format_date(start), format_date(end))).json()

        for row in json_response:
            # Create a call object w/ the SQLAlchemy Model
            # Thankfully, we have a function that'll do just that. So let's call it.
            call = self.format_call(row)

            # Apparently these calls have like zero info on them
            if (call.lat, call.lon) != (-361, -361):

                # If this call exists already, set the existing id as the new one
                # and if we were on 3.8, we could use the := operator and save a line :(
                existing_id = CallQuery.get_existing_id(call)
                if existing_id:
                    call.id = existing_id

                # We want to merge the calls because new data may have popped up for the call
                # (like address)
                self.db.session.merge(call)

        # I'm not flushing after each one because I think that SQLAlchemy auto flushes
        self.db.session.commit()

    def format_call(self, row: dict) -> Call:
        '''
        Takes raw data from the scraper and puts it into a Call object
        '''
        # Create a naive timestamp from the date (DispatchTime) and time (DispatchTime2)
        timestamp = datetime.strptime(row['DispatchTime'] + '' + row['DispatchTime2'],
                                      '%m-%d-%Y%H:%M:%S')
        # Then make it UTC, with the convert function in the parent
        timestamp = self.convert_naive_utc(timestamp)

        lat = float(row['lat'])
        lon = float(row['lon'])

        return Call(timestamp, lat, lon, row['City'], row['CallType'], row['Address'])
