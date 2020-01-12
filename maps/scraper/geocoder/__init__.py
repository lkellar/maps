"""
Geo-coding module converts addresses into latitude/longitude using Bing Maps API

Why Bing?
    Bing allows first 50,000 requests a year free, unlike Google, which has no free tier.
    Bing also has a not-for-profit plan, which has much higher limits for free
"""
import time

from .jobmanager import JobManager
from .settings import GeocodeDataflow


# ------------------------------ GEO-CODING FUNCTIONS ------------------------------


def geocode_lookup(addresses: [str]) -> dict:
    """
    This function uses Bing's geocodeLookup service to get lat/long from addresses.

    :param addresses: List of all the addresses to geocode.
    :return: a dict of addresses -> (lat, lon)
    """

    job_manager = JobManager()

    while addresses:
        # Select first 50 addresses
        batch = addresses[:50]
        del addresses[:50]

        # Start a job
        job_manager.create(batch)
        # Wait for job completion
        while not job_manager.check_completed():
            time.sleep(5)

        # Fetch job results
        job_manager.fetch_results()

    return job_manager.address_to_coord
