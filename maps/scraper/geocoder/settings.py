"""
Settings for the Geocoder module
"""
from flask import current_app


# ------------------------------ General Bing Maps API configuration ------------------------------

# Define key parameters necessary for API request
KEY_PARAMS = {
    "key": current_app.config.get("BING_MAPS_KEY")
}


# ------------------------------ Geocode Dataflow API configuration ------------------------------
# An API within Bing Maps. See docs at
# https://docs.microsoft.com/en-us/bingmaps/spatial-data-services/geocode-dataflow-api/geocode-dataflow-data-schema-version-2-0


class GeocodeDataflow:
    # Request format: id|Address.AddressLine|Address.Locality|Address.AdminDistrict|Address.CountryRegion\n
    FIELDS = (
        # Define input fields for our geo-coding request
        'Id',
        'GeocodeRequest/Address/AddressLine',  # address
        'GeocodeRequest/Address/PostalCode',  # Zip Code
        'GeocodeRequest/Address/AdminDistrict',  # state
        'GeocodeRequest/Address/CountryRegion',  # country

        # Define Response fields latitude and longitude
        'GeocodeResponse/Point/Latitude',
        'GeocodeResponse/Point/Longitude',
        'GeocodeResponse/Address/Locality'  # City
    )
    # Generate our schema for geo-coding requests and responses to the Dataflow API
    HEADING = 'Bing Spatial Data Services, 2.0\n' + '|'.join(FIELDS)
