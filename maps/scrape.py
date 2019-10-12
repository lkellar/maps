import requests
from datetime import datetime, timedelta
import sqlite3

from maps.config import *


def format_date(dt: datetime):
    return dt.strftime("%Y-%m-%d")


def scrape_calls(date1: datetime, date2: datetime):
    url = "https://maps.fayetteville-ar.gov/DispatchLogs/json/getIncidents.cshtml/{}/{}"
    r = requests.get(url.format(format_date(date1), format_date(date2)))
    j = r.json()
    return j


def insert_data(calls):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        prepared = []
        for call in calls:
            dt = datetime.strptime(call["DispatchTime"] + " " + call["DispatchTime2"], "%m-%d-%Y %H:%M:%S")
            values = (dt, call["lat"], call["lon"], call["City"], call["CallType"], call["Address"])
            prepared.append(values)
        c.executemany('''INSERT OR REPLACE INTO calls (datetime, lat, lon, city, call_type, address)
        VALUES (?,?,?,?,?,?)''', prepared)

    conn.commit()


def fetch_data(days_ago=1):
    today = datetime.today()
    data = scrape_calls(today - timedelta(days=days_ago), today + timedelta(days=1))
    insert_data(data)


if __name__ == '__main__':
    fetch_data(1)
