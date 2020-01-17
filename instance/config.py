"""
Define instance-specific configuration.
The instance folder is designed to not be under version control and be deployment specific.
"""


# An API key for the Bing Maps Geocode Dataflow API.
# It's required for cities like Springdale which don't provide coordinates.
BING_MAPS_KEY = None

# A DSN for sentry. If provided, sentry error reporting is set up.
MAPS_SENTRY_DSN = None
