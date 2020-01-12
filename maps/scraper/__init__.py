from datetime import datetime, timedelta
from flask import current_app

import maps.scraper.fayetteville as fayetteville
import maps.scraper.springdale as springdale


def scrape_fayetteville(days):
    today = datetime.today()
    fayetteville.scrape_to_db(today - timedelta(days=days), today + timedelta(days=1))


def scrape_springdale():
    # ONLY DO IT IF WE HAVE BING MAPS KEY
    if current_app.config.get('BING_MAPS_KEY'):
        # Springdale doesn't do dates, they only give past 24 hours
        springdale.scrape_to_db()
    else:
        print('No Bing Maps Key, so no springdale for you')

