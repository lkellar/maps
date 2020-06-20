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


def geocode_lookup_city(addressCities: [dict]) -> dict:
    """
    This function uses Bing's geocodeLookup service to get lat/lon and city from addresses.

    :param addressCities: list of dicts with following format {address: str, city: str} (if this was typescript, I could set this as the type smh)
    :return: a dict of addresses -> (lat, lon)
    """

    if not current_app.config.get("BING_MAPS_KEY"):
        raise BingKeyNotFound()

    job_manager = JobManager()

    while addressCities:
        # Select first 50 addresses
        batch = addressCities[:50]
        del addressCities[:50]

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
    :return: a dict of addresses -> (lat, lon)
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

