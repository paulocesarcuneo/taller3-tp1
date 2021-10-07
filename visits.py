from os import environ
from google.cloud import datastore

DB = datastore.Client(environ.get("PROJECT_ID", "taller3-pcuneo"))


def inc_visits(page_name):
    with DB.transaction():
        page_counter = DB.get(DB.key("page", page_name))
        visits = page_counter["visits"]
        page_counter["visits"] = visits + 1
        DB.put(page_counter)


def get_visits(page_name):
    page_counter = DB.get(DB.key("page", page_name))
    total = page_counter["visits"]
    return str(total)
