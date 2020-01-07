#pylint: disable=anomalous-backslash-in-string, line-too-long, no-member, pointless-string-statement
#pylint: disable=too-many-locals
# You may be thinking, why does Lucas disable so many pylint
from dataclasses import dataclass
from datetime import datetime
import time
import os
import requests

from maps import db
from maps.models import Call, CallQuery
from maps.scraper.base import BaseScraper

@dataclass
class SpringdaleMockCall:
    '''
    A dataclass to standardize the mock calls checked against the db

    timestamp (datetime): A UTC timestamp of when the event took place
    address (str): The given address where the event took place
    call_type (str): The type of call made
    disposition (str): The DISPOSITION of the call, I think it means status
    '''
    timestamp: datetime
    address: str
    call_type: str
    dispositon: str

class SpringdaleScraper(BaseScraper):
    def __init__(self, db):
        # Interesting thing about springdale. It's a .txt extension, but it's in JSON format
        # Also, regardless of parameters, only the past 24 hours are shown.
        self.url = 'https://ww2.springdalear.gov/web_includes/dispatch_logs.txt'
        self.bing_maps_key = os.environ.get('BING_MAPS_KEY')
        self.timezone = 'America/Chicago'
        self.db = db

        # We gotta initilizate the Base Scraper!
        super().__init__(self.timezone)

    def scrape(self):
        '''
        Scrape Springdale Calls

        No params, this function just returns the past 24 hours of calls
        This is because Springdale's system only lets the public see the past 24 hours of content.
        ¯\_(ツ)_/¯

        Returns: NOTHING. All calls are sent to DB

        Also, this function will raise errors, mostly with bing maps api. I suggest having a
        try/except at a higher level, sending errors to sentry, then continuing on, because if
        springdale fails, there's no reason to ignore fayetteville
        '''

        # First make sure we have the bing_maps_key.
        # If the bing_maps_key isn't found, this is bad
        if not self.bing_maps_key:
            raise BingKeyNotFound()

        json_response = requests.get(self.url).json()

        # The items are in a "demo" object, also implying there is much more data somewhere else,
        # and this url is just "demoing" from the large DB. Of course, with enough scraping, we can
        # make our own large db over time
        json_response = json_response['demo']


        # Okay, so the plan is to iterate over all the calls, update the ones that have already been
        # added, and the new ones, we get their coordinates
        '''
        Springdale's response objects have the following schema
        [
            %m/%d %H:%M:%S,
            CALL_TYPE,
            ADDRESS,
            DISPOSITION (which I guess is status)
        ]

        Also, pylint called this a "pointless-string-statement", like if you disagree
        '''
        new_calls = []

        for event in json_response:
            # DOn't do anything if there is no address
            if event[2]:
                # Generate the UTC timestamp, and make a mock call
                timestamp = self.generate_timestamp(event[0])
                mock_call = SpringdaleMockCall(timestamp, event[2], event[1], event[3])

                existing_call = CallQuery.get_existing_call(mock_call)

                if existing_call:
                    # Update the disposition, as it's the only thing that would change
                    # Because I seriously doubt, somehow the city would change (espec because we set
                    # that manually)
                    existing_call.notes = event[3]
                else:
                    # Well, If we've got ourselves a new call, let's go ahead and add it to the
                    # new_calls list, innovative right?
                    new_calls.append(mock_call)

        # Let's save our changes before we move onto the bing time
        # Also, pylint won't shut up about how it thinks the scopedsession or whatever has no commit
        # member. It does, so I added a no-member disable at the top.
        db.session.commit()

        # If there are no new calls, no point the geocoding stuff
        if not new_calls:
            return

        addresses = [i.address for i in new_calls]

        # removing duplicates by converting to set and list back
        addresses = list(set(addresses))

        address_coords = {}

        if len(addresses) <= 50:
            # turn theses addresses into coordinates
            address_coords = self.geocode_lookup(addresses)
        else:
            # Since we have over 50 addresses, do it 50 at a time
            while addresses:
                # Select 50 addresses
                batch = addresses[:50]
                # Calculate them and add them
                address_coords = {**address_coords, **self.geocode_lookup(batch)}
                # Then destroy them
                del addresses[:50]

        for mock_call in new_calls:
            # First, lets lookup the coordinates for the address from our response
            coords = address_coords[mock_call.address]

            # let's make a call, lat comes first, then long. Remember it with this great rhyme:
            # Lat comes first / lon doesn't come first.
            # Also, I'm throwing disposition in the slot for notes
            call = Call(mock_call.timestamp, coords[0], coords[1], 'Springdale',
                        mock_call.call_type, mock_call.address, mock_call.dispositon)

            # So, technically a merge is overkill here, because all of these calls are new
            # BUT, better safe than sorry, and more importantly, we use merge in the other scraper,
            # and consistency is key. Key to what? I don't know, I think it's a riddle
            self.db.session.merge(call)

        # After this, we commit, and are done, isn't that great?
        self.db.session.commit()

    def geocode_lookup(self, addresses: [str]) -> dict:
        '''
        This function uses Bing's geocodeLookup service to get lat/long from addresses.

        I'm using Bing because they allow first 50,000 requests a year to be free, and I have a
        microsoft account, unlike goog, where I don't have a goog account, and they have no free
        tier.

        Finally, in need of expansion, Bing has a not-for-profit plan, which has much higher limits
        for free, as long as we don't charge people money (which we shouldn't)

        addresses (str): Literally a list of all the addresses. LIMIT 50 ADDRESSES

        Returns: a dict of addresses to coordinates with the following format.
            {ADDRESS: (LATITUDE, LONGITUDE)}
        '''

        if len(addresses) > 50:
            return ValueError(f'Only 50 addresses at a time. You provided {len(addresses)} addresses')

        # Creating a session, because why not, I think it's more efficient for the same host
        s = requests.session()

        # The header for our geocoding request. See docs at
        # https://docs.microsoft.com/en-us/bingmaps/spatial-data-services/geocode-dataflow-api/geocode-dataflow-data-schema-version-2-0
        # header = id|Address.AddressLine|Address.Locality|Address.AdminDistrict|Address.CountryRegion\n

        formatted_addresses = []
        # Now, with each address, format each according to the header
        header = 'Bing Spatial Data Services, 2.0\nId| GeocodeRequest/Address/AddressLine| GeocodeRequest/Address/Locality| GeocodeRequest/Address/AdminDistrict| GeocodeRequest/Address/CountryRegion| GeocodeResponse/Point/Latitude| GeocodeResponse/Point/Longitude'
        for counter, add in enumerate(addresses):
            line = f'{counter}|{add}|Springdale|AR|US'
            formatted_addresses.append(line)

        request_body = header + '\n' + '\n'.join(formatted_addresses)

        params = {
            'input': 'pipe',
            'key': self.bing_maps_key,
            'output': 'json'
        }

        # Create a geocoding-job w/ Bing maps
        create_response = s.post('https://spatial.virtualearth.net/REST/v1/Dataflows/Geocode', params=params,
                                 headers={'Content-Type': 'text/plain'}, data=request_body).json()

        if create_response['statusCode'] == '400':
            # if there is an error creating the job, raise an error! Yay
            raise BingAPIError(create_response['errorDetails'])

        # This is where to find the job id, crazy right?
        job_id = create_response['resourceSets'][0]['resources'][0]['id']

        completed_url = None
        # Hey, let's check job status, til it's done
        while not completed_url:
            status_response = s.get(f'https://spatial.virtualearth.net/REST/v1/Dataflows/Geocode/{job_id}',
                                    params={'key': self.bing_maps_key, 'output': 'json'}).json()

            # Remember this long json tree from somewhere?
            if status_response['resourceSets'][0]['resources'][0]['status'] == 'Completed':
                completed_url = status_response['resourceSets'][0]['resources'][0]['links'][1]['url']
                if 'succeeded' not in completed_url:
                    raise BingAPIError(f'Here\'s the URL that shouldn\'ve been succeeded {completed_url}')
            else:
                # Look, if it's not done yet, we gotta wait, patience is key
                time.sleep(5)

        # It is time to download those hot new addresses. Exciting right? Almost as exciting as
        # getting a dell
        results = s.get(completed_url, params={'key': self.bing_maps_key}).text

        # Split into list
        results = results.split('\n')

        # And remove empty lines
        results = list(filter(None, results))

        # Remove the header
        results = results[2:]

        addresses = {}
        for result in results:
            # Split line up into list by pipe seperator, then remove empty strings
            result = result.split('|')
            result = list(filter(None, result))

            # Result schema follows header
            # Lat and lon are 5th and 6th in the array, so float and tuple them
            coordinates = (float(result[5]), float(result[6]))
            # result[1] is the address, and this makes a dict that conforms with the thingy at the
            # top of the function
            addresses[result[1]] = coordinates

        # return the finished addresses
        return addresses

    def generate_timestamp(self, datetime_str: str) -> datetime:
        '''
        Takes raw data from the scraper and creates a timestamp out of it

        Returns: datetime object, utc timestamp
        '''
        # Since springdale doesn't come w/ year, we provide our own
        row_year = datetime.now().year

        # If it's january, and we have results from december, we know that the results must be from
        # the past 24 hours, so we know those dec results are from the previous year, so we subtract
        # one year
        if datetime.now().month == 1 and datetime_str.split('/')[0] == '12':
            row_year -= 1

        # Chunk the generated year on the front, and create a naive timestamp
        timestamp = datetime.strptime(f'{row_year}/{datetime_str}', '%Y/%m/%d %H:%M:%S')

        # Then make it utc with convert func in parent
        return self.convert_naive_utc(timestamp)


class BingKeyNotFound(BaseException):
    '''
    An exception class to use when the Bing API Key isn't found
    '''

class BingAPIError(BaseException):
    '''
    An exception class to use when the Bing API throws an error
    '''
