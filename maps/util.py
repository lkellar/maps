from datetime import datetime
import pytz

from maps import app


def convert_naive_to_db(naive: datetime, local_tz: pytz.timezone) -> datetime:
    """
    This function inputs a naive datetime, attaches the given (local) timezone to it,
    then converts it to the database timezone

    Returns: a database timezone datetime
    """

    # attach proper timezone for the date (fayetteville.gov for example uses America/Chicago)
    dt = local_tz.localize(naive)

    # convert to database timezone
    dt = dt.astimezone(app.config['TIMEZONE'])
    return dt
