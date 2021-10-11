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


# def inc_visits(page_name):
#     nshard = random.randint(0, N_SHARDS - 1)
#     entity_inc_visits(f"{page_name}_{nshard}")


# def get_visits(page_name):
#     total = 0
#     shards = list(DB.query(kind="page").add_filter("group", "=", page_name).fetch())
#     for shard in shards:
#         total += shard["visits"]
#     return str(total)


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


import threading
from datetime import datetime, timedelta


class Batch:
    BATCH_MAX = int(environ.get("BATCH_MAX", 100))
    batch = dict()
    batch_count = 0
    lastupdate_datetime = datetime.now()
    nextupdate_datetime = datetime.now()
    lock = threading.RLock()

    def _inc_count(self, key):
        self.batch_count += 1
        if key in self.batch:
            self.batch[key] += 1
        else:
            self.batch[key] = 1

    def _should_update(self):
        return (
            self.nextupdate_datetime < datetime.now()
            or self.batch_count > self.BATCH_MAX
        )

    def _push_updates(self):
        result = []
        entities = list(DB.query(kind="page").fetch())
        for entity in entities:
            key = entity.key.id_or_name
            if key in self.batch:
                entity["visits"] += self.batch[key]
                result.append(entity)
        DB.put_multi(result)
        self.nextupdate_datetime = datetime.now() + timedelta(seconds=10)
        self.batch_count = 0
        self.batch = dict()

    def inc_visits(self, page_name):
        with self.lock:
            self._inc_count(page_name)
            if self._should_update():
                self._push_updates()


BATCHER = Batch()
