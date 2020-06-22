"""
Geo-coding module converts addresses into latitude/longitude using Bing Maps API

Why Bing?
    Bing allows first 50,000 requests a year free, unlike Google, which has no free tier.
    Bing also has a not-for-profit plan, which has much higher limits for free
"""
from flask import current_app

from .jobmanager import JobManager
from .exceptions import BingKeyNotFound, BingStallError


# ------------------------------ GEO-CODING FUNCTIONS ------------------------------


def geocode_lookup_city(addresses_cities: [dict]) -> dict:
    """
    This function uses Bing's geocodeLookup service to get lat/lon and city from addresses.

    :param addresses_cities: list of dicts with following format {address: str, city: str}
    :return: a dict of addresses -> (lat, lon, city)
    """

    if not current_app.config.get("BING_MAPS_KEY"):
        raise BingKeyNotFound()

    job_manager = JobManager()

    while addresses_cities:
        # Select first 50 addresses
        batch = addresses_cities[:50]
        del addresses_cities[:50]

        # Start a job
        job_manager.create_city_job(batch)
        # Wait for job completion
        job_manager.wait_for_completion()

        # Fetch job results
        job_manager.fetch_results()

    return job_manager.address_to_geocode


def geocode_lookup_zipcode(addresses: [str], zipcode: str) -> dict:
    """
    This function uses Bing's geocodeLookup service to get lat/lon and city from addresses.

    :param addresses: List of all the addresses to geocode.
    :param zipcode: Zip code shared by addresses, helps geocoder find correct location
    :return: a dict of addresses -> (lat, lon, city)
    """

    if not current_app.config.get("BING_MAPS_KEY"):
        raise BingKeyNotFound()

    job_manager = JobManager()

    while addresses:
        # Select first 50 addresses
        batch = addresses[:50]
        del addresses[:50]

        # Start a job
        job_manager.create_zipcode_job(batch, zipcode)
        # Wait for job completion
        job_manager.wait_for_completion()

        # Fetch job results
        job_manager.fetch_results()

    return job_manager.address_to_geocode

