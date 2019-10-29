from maps import app, db
from maps.models import Call, CallQuery
import requests
from datetime import datetime, timedelta

import click


def format_date(dt: datetime):
    return dt.strftime("%Y-%m-%d")


def scrape_calls(date1: datetime, date2: datetime):
    url = "https://maps.fayetteville-ar.gov/DispatchLogs/json/getIncidents.cshtml/{}/{}"
    r = requests.get(url.format(format_date(date1), format_date(date2)))
    j = r.json()
    return j


def insert_data(call_data, v=0):
    for row_data in call_data:
        call = None
        try:
            call = Call(row_data)
        except Exception as e:
            app.logger.warning('Scraper: {}'.format(e))
        if call:
            existing_id = CallQuery.get_existing_id(call)
            if existing_id is not None:
                call.id = existing_id
                if v >= 2:
                    app.logger.info('Scraper: Merging {} into existing Call'.format(call))
            elif v >= 1:
                app.logger.info('Scraper: Adding new call {}'.format(call))
            db.session.merge(call)
            db.session.flush()
    db.session.commit()


@click.command()
@click.argument('days', default=1)
def scrape(days):
    today = datetime.today()
    data = scrape_calls(today - timedelta(days=days), today + timedelta(days=1))
    insert_data(data, 1)


if __name__ == '__main__':
    db.create_all()
    scrape()
