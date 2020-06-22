"""
Settings for the Geocoder module
"""
from flask import current_app
from abc import ABC, abstractmethod

# ------------------------------ General Bing Maps API configuration ------------------------------

# Define key parameters necessary for API request
KEY_PARAMS = {
    "key": current_app.config.get("BING_MAPS_KEY")
}


# ------------------------------ Geocode Dataflow API configuration ------------------------------
# An API within Bing Maps. See docs at
# https://docs.microsoft.com/en-us/bingmaps/spatial-data-services/geocode-dataflow-api/geocode-dataflow-data-schema-version-2-0


RequestField = {
    'ID':      'Id',
    'ADDRESS': 'GeocodeRequest/Address/AddressLine',
    'ZIPCODE': 'GeocodeRequest/Address/PostalCode',
    'CITY':    'GeocodeRequest/Address/Locality',
    'STATE':   'GeocodeRequest/Address/AdminDistrict',
    'COUNTRY': 'GeocodeRequest/Address/CountryRegion'
}
ResponseField = {
    'LAT':  'GeocodeResponse/Point/Latitude',
    'LON':  'GeocodeResponse/Point/Longitude',
    'CITY': 'GeocodeResponse/Address/Locality'
}


class GeocodeDataflow(ABC):
    def __init__(self, k):
        self.FIELDS = [
            # Define input fields for our geo-coding request
            RequestField['ID'],
            RequestField['ADDRESS'],
            RequestField[k],
            RequestField['STATE'],
            RequestField['COUNTRY'],

            # Define Response fields latitude, longitude, city
            ResponseField['LAT'],
            ResponseField['LON'],
            ResponseField['CITY']
        ]

        # Generate our schema for geo-coding requests and responses to the Dataflow API
        self.HEADING = 'Bing Spatial Data Services, 2.0\n' + '|'.join(self.FIELDS)


class GeocodeDataflowCity(GeocodeDataflow):
    def __init__(self):
        super().__init__('CITY')

    def format_address(self, id_, address, city, state='AR', country='US'):
        """ Format geocode request body according to our Geocode Dataflow heading """
        return f'{id_}|{address}|{city}|{state}|{country}'

    def generate(self, addresses_cities):
        # Format each address according to our heading
        formatted_addresses = [self.format_address(idx, item['address'], city=item['city'])
                               for idx, item in enumerate(addresses_cities)]

        # Generate input data to post in the body of the request
        return self.HEADING + '\n' + '\n'.join(formatted_addresses)


class GeocodeDataflowZipCode(GeocodeDataflow):
    def __init__(self):
        super().__init__('ZIPCODE')

    def format_address(self, id_, address, zipcode, state='AR', country='US'):
        """ Format geocode request body according to our Geocode Dataflow heading """
        return f'{id_}|{address}|{zipcode}|{state}|{country}'

    def generate(self, addresses, zipcode):
        # Format each address according to our heading
        formatted_addresses = [self.format_address(idx, address, zipcode=zipcode)
                               for idx, address in enumerate(addresses)]

        # Generate input data to post in the body of the request
        return self.HEADING + '\n' + '\n'.join(formatted_addresses)


GDCity = GeocodeDataflowCity()
GDZipCode = GeocodeDataflowZipCode()

