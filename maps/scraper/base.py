from datetime import datetime
import pytz


def convert_naive_utc(naive: datetime, timezone: pytz.timezone) -> datetime:
    """
    This function inputs a naive timezone, applies the local timezone to it,
    then changes it to a UTC timestamp

    Returns: a UTC time zone datetime
    """

    # attach proper timezone for the date (fayetteville.gov for example uses America/Chicago)
    dt = timezone.localize(naive)

    # convert to UTC timezone
    dt = dt.astimezone(pytz.UTC)
    return dt
