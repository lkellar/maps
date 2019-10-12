from os import path

APP_PATH = path.dirname(path.realpath(__file__))


DB_PATH = path.join(APP_PATH, "../data.sqlite")

TIMEZONE = "America/Chicago"
