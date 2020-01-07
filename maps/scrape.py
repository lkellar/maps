from datetime import datetime, timedelta

import click

from maps import db
from maps.scraper.fayetteville import FayettevilleScraper
from maps.scraper.springdale import SpringdaleScraper

@click.command()
@click.argument('days', default=1)
def scrape(days):
    today = datetime.today()
    f = FayettevilleScraper(db)
    f.scrape(today - timedelta(days=days), today + timedelta(days=1))

    # Springdale doesn't do dates, they only give past 24 hours
    s = SpringdaleScraper(db)
    s.scrape()

if __name__ == '__main__':
    db.create_all()

    #pylint: disable=no-value-for-parameter
    scrape()
