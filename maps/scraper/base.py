from abc import ABC
from datetime import datetime
import pytz

class BaseScraper(ABC):
    def __init__(self, timezone: str):
        self.timezone = pytz.timezone(timezone)

    def convert_naive_utc(self, naive: datetime) -> datetime:
        '''
        This function inputs a naive timezone, applies the local timezone to it,
        then changes it to a UTC timestamp

        Returns: a UTC time zone datetime
        '''

        # attach proper timezone for the date (fayetteville.gov for example uses America/Chicago)
        dt = self.timezone.localize(naive)

        # convert to UTC timezone
        dt = dt.astimezone(pytz.UTC)
        return dt
