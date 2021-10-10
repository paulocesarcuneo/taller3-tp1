from http.client import HTTPMessage
from os import environ
from google.cloud import datastore
import random

DB = datastore.Client(environ.get("PROJECT_ID", "taller3-pcuneo"))

N_SHARDS = int(environ.get("N_SHARDS", "10"))


def inc_visits(page_name):
    nshard = random.randint(0, N_SHARDS - 1)
    shard = f"{page_name}_{nshard}"
    with DB.transaction():
        page_counter = DB.get(DB.key("page", shard))
        visits = page_counter["visits"]
        page_counter["visits"] = visits + 1
        DB.put(page_counter)


def get_visits(page_name):
    shards = list(DB.query(kind="page").add_filter("group", "=", page_name).fetch())
    total = 0
    for shard in shards:
        total += shard["visits"]
    # page_counter = DB.get(DB.key("page", page_name))
    # total = page_counter["visits"]
    return str(total)


def init_visits(nshards=N_SHARDS):
    pages = ["home", "jobs", "offices", "about", "legals"]
    for page in pages:
        for nshard in range(nshards):
            shard = datastore.Entity(
                key=DB.key("page", f"{page}_{nshard}"), exclude_from_indexes=["visits"]
            )
            shard["group"] = page
            shard["visits"] = 0
            with DB.transaction():
                DB.put(shard)
