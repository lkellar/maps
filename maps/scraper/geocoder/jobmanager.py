"""
Class to encapsulate geo-coding jobs in the Geocode Dataflow API.
See API documentation:
    https://docs.microsoft.com/en-us/bingmaps/spatial-data-services/geocode-dataflow-api/
"""
import time
import requests

from .exceptions import BingAPIError, BingStallError, BingTimeoutError
from .settings import GDZipCode, GDCity, KEY_PARAMS


# ------------------------------ API REQUEST WRAPPERS ------------------------------

# Creating a session, probably more efficient for the same host
session = requests.session()


def update_params(params):
    if params is None:
        params = KEY_PARAMS
    else:
        params.update(KEY_PARAMS)
    return params


def request_post(*args, params=None, **kwargs):
    params = update_params(params)
    try:
        return requests.post(*args, params=params, **kwargs)
    except requests.ConnectionError:
        # See notes in request_get
        raise BingTimeoutError()


def request_get(*args, params=None, **kwargs):
    params = update_params(params)
    try:
        return requests.get(*args, params=params, **kwargs)
    except requests.ConnectionError:
        # Something broke on Bing Maps API end, happens a couple times a month. No worries though, we'll just grab it on the next run
        # Interesting bit is, it usually happens in batches, like 5 in a day, then nothing for a couple weeks, I guess just bing maps outages, or something with our account
        # Problem is always resolved by just trying again later though
        raise BingTimeoutError()


# ------------------------------ GEO-CODING RESULT CLASS ------------------------------

class Result:
    def __init__(self, row):
        # Split line up into list by pipe separator, then remove empty strings
        values = row.split('|')
        values = list(filter(None, values))

        # Set properties in order (result follows heading schema)
        self.id, self.address, self.zipOrCityInput, self.state, self.country, self.lat, self.lon, self.city = values


# ------------------------------ JOB MANAGER ------------------------------

class JobManager:
    def __init__(self):
        self.job_id = None
        self.completed_url = None

        self.results: [Result] = []
        self.address_to_geocode = {}

    def create_city_job(self, addresses_cities: list):
        """
        Start the job based on cities
        :param addresses_cities: list of dicts with following format {address: str, city: str} (LIMIT 50)
        """
        if len(addresses_cities) > 50:
            raise ValueError(f'Only 50 addresses at a time. You provided {len(addresses_cities)} addresses')

        input_data = GDCity.generate(addresses_cities)
        self.create_job_internal(input_data)

    def create_zipcode_job(self, addresses: list, zipcode: str):
        """
        Start the job based on zipcode
        :param addresses: list of addresses to geocode (LIMIT 50 ADDRESSES)
        :param zipcode: Zipcode to send to bing maps
        """
        if len(addresses) > 50:
            raise ValueError(f'Only 50 addresses at a time. You provided {len(addresses)} addresses')

        input_data = GDZipCode.generate(addresses, zipcode)
        self.create_job_internal(input_data)
        
    def create_job_internal(self, input_data: str):
        params = {
            'input': 'pipe',  # We are using pipe (|) as a separator in our input data
            'output': 'json',  # We want the output format to be JSON
        }
        # Create a geo-coding job w/ Geocode Dataflow API
        res = request_post('https://spatial.virtualearth.net/REST/v1/Dataflows/Geocode',
                           params=params,
                           headers={'Content-Type': 'text/plain'},
                           data=input_data)
        response_json = res.json()

        # if there's an error creating the job, raise an error
        if int(response_json['statusCode']) >= 400:
            if "JobUsageQuota: Account already has 3 'Pending' jobs" in response_json['errorDetails']:
                raise BingStallError(response_json['errorDetails'])

            raise BingAPIError(response_json['errorDetails'])

        # Get job's id so we can check its status and get result
        self.job_id = response_json['resourceSets'][0]['resources'][0]['id']

    def check_completed(self):
        """
        Check job status
        :return: True if job is completed, else False
        """
        res = request_get(f'https://spatial.virtualearth.net/REST/v1/Dataflows/Geocode/{self.job_id}',
                          params={'output': 'json'})
        response_json = res.json()

        # Extract status of job from json
        status = response_json['resourceSets'][0]['resources'][0]['status']

        if status == 'Aborted':
            raise BingAPIError("Job was aborted due to an error.")
        if status == 'Completed':
            # If completed, get url to results
            self.completed_url = response_json['resourceSets'][0]['resources'][0]['links'][1]['url']
            return True
        return False

    def wait_for_completion(self, timeout=600):
        """
        Wait for job completion
        :param timeout: minimum number of seconds to wait before timing out
        """
        total = 0
        s = 5
        while not self.check_completed():
            # Give up after certain amount of time
            if total > timeout:
                raise BingTimeoutError(f'Job failed to complete after {total} seconds')

            time.sleep(s)  # Get status every s seconds
            total += s
            s += 1  # Increase interval over time so we make less requests

    def fetch_results(self):
        """ Fetch results of completed job and process results to dictionary of addresses -> (lat, lon) """
        if 'succeeded' not in self.completed_url:
            raise BingAPIError(f'Job result url should have contained "succeeded" at {self.completed_url}')

        # It is time to download those hot new addresses. Exciting right? Almost as exciting as getting a dell
        results_txt = request_get(self.completed_url).text

        # Split into list
        rows = results_txt.split('\n')
        # Remove empty lines
        rows = list(filter(None, rows))
        # Remove the header
        rows = rows[2:]

        for row in rows:
            result = Result(row)
            self.results.append(result)
            self.address_to_geocode[result.address] = {'lat': result.lat, 'lon': result.lon,
                                                       'city': result.city.rstrip('\r')}
