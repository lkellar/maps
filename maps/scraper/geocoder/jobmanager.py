"""
Class to encapsulate geo-coding jobs in the Geocode Dataflow API.
See API documentation:
    https://docs.microsoft.com/en-us/bingmaps/spatial-data-services/geocode-dataflow-api/
"""
import requests

from .exceptions import BingAPIError
from .settings import GeocodeDataflow, KEY_PARAMS


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
    return requests.post(*args, params=params, **kwargs)


def request_get(*args, params=None, **kwargs):
    params = update_params(params)
    return requests.get(*args, params=params, **kwargs)


# ------------------------------ GEO-CODING RESULT CLASS ------------------------------

class Result:
    def __init__(self, row):
        # Split line up into list by pipe separator, then remove empty strings
        values = row.split('|')
        values = list(filter(None, values))

        # Set properties in order (result follows heading schema)
        # Zipcode will be inaccurate most likely, pls ignore it
        self.id, self.address, self.zipcode, self.state, self.country, self.lat, self.lon, self.city = values

        self.coord = (self.lat, self.lon)


def format_address(id_, address, zipcode=72764, state='AR', country='US'):
    """ Format geocode request body according to our Geocode Dataflow heading """
    return f'{id_}|{address}|{zipcode}|{state}|{country}'


# ------------------------------ JOB MANAGER ------------------------------

class JobManager:
    def __init__(self):
        self.job_id = None
        self.completed_url = None

        self.results: [Result] = []
        self.address_to_geocode = {}

    def create(self, addresses):
        """
        Start the job
        :param addresses: list of addresses to geocode (LIMIT 50 ADDRESSES)
        """
        if len(addresses) > 50:
            return ValueError(f'Only 50 addresses at a time. You provided {len(addresses)} addresses')

        # Format each address according to our heading
        formatted_addresses = [format_address(idx, address) for idx, address in enumerate(addresses)]

        # Generate input data to post in the body of the request
        input_data = GeocodeDataflow.HEADING + '\n' + '\n'.join(formatted_addresses)

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

        if response_json['statusCode'] == '400':
            # if there's an error creating the job, raise an error! Yay
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
        if status == 'Completed':
            # If completed, get url to results
            self.completed_url = response_json['resourceSets'][0]['resources'][0]['links'][1]['url']
            return True
        return False

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
            self.address_to_geocode[result.address] = {'coord': result.coord, 'city': result.city.rstrip('\r')}

