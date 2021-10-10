from os import environ
from google.cloud import datastore

DB = datastore.Client(environ.get("PROJECT_ID", "taller3-pcuneo"))


def entity_inc_visits(key):
    with DB.transaction():
        page_counter = DB.get(DB.key("page", key))
        visits = page_counter["visits"]
        page_counter["visits"] = visits + 1
        DB.put(page_counter)


def inc_visits(page_name):
    entity_inc_visits(page_name)


def get_visits(page_name):
    page_counter = DB.get(DB.key("page", page_name))
    total = page_counter["visits"]
    return str(total)


# import random
# N_SHARDS = int(environ.get("N_SHARDS", "10"))


# def sharded_inc_visits(page_name):
#     nshard = random.randint(0, N_SHARDS - 1)
#     entity_inc_visits(f"{page_name}_{nshard}")


# def sharded_get_visits(page_name):
#     total = 0
#     shards = list(DB.query(kind="page").add_filter("group", "=", page_name).fetch())
#     for shard in shards:
#         total += shard["visits"]
#     return total


def init_visits(nshards):
    pages = ["home", "jobs", "offices", "about", "legals"]
    for page in pages:
        if nshards:
            for nshard in range(nshards):
                shard = datastore.Entity(
                    key=DB.key("page", f"{page}_{nshard}"),
                    exclude_from_indexes=["visits"],
                )
                shard["group"] = page
                shard["visits"] = 0
                with DB.transaction():
                    DB.put(shard)
        else:
            entity = datastore.Entity(
                key=DB.key("page", page),
                exclude_from_indexes=["visits"],
            )
            entity["group"] = page
            entity["visits"] = 0
            with DB.transaction():
                DB.put(entity)


# BATCH = dict()


# def inc_batch(page_name):
#     global BATCH
#     if time_elapsed:
#         entities = list(DB.query(kind="page").fetch())
#         for entity in entities:
#             if entity["name"] in BATCH:
#                 entity["visits"] += BATCH[entity["name"]]
#             if entity["name"] == page_name:
#                 entity["visits"] += 1
#         DB.put_multi(entities, retry=10)
#         BATCH = dict()
#     else:
#         if page_name in BATCH:
#             BATCH[page_name] += 1
#         else:
#             BATCH[page_name] = 1
