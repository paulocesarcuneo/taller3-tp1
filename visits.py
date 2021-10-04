import base64
from os import environ
from google.cloud import datastore

PROJECT_ID = environ.get("PROJECT_ID", "taller3-pcuneo")


def inc_visits(event, context):
    page_name = base64.b64decode(event["data"]).decode("utf-8")
    db = datastore.Client(PROJECT_ID)
    with db.transaction():
        page_counter = db.get(db.key("page", page_name))
        visits = page_counter["visits"]
        page_counter["visits"] = visits + 1
        db.put(page_counter)


db = datastore.Client(PROJECT_ID)


def get_visits(request):
    page_name = request.args.get("page_name")
    page_counter = db.get(db.key("page", page_name))
    total = page_counter["visits"]
    return str(total)


def post_visits(request):
    page_name = request.get_json()["page_name"]
    with db.transaction():
        page_counter = db.get(db.key("page", page_name))
        visits = page_counter["visits"]
        page_counter["visits"] = visits + 1
        db.put(page_counter)
    return "Ok"


# from google.cloud import pubsub_v1

# TOPIC_ID = environ.get("TOPIC_ID", "visits")
# publisher = pubsub_v1.PublisherClient()


# def post_visits_pubsub(request):
#     payload = request.get_json()
#     page_name = payload["page_name"]
#     topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
#     message_bytes = page_name.encode("utf-8")
#     try:
#         publish_future = publisher.publish(topic_path, data=message_bytes)
#         publish_future.result()
#         return "Message published."
#     except Exception as e:
#         print(e)
#         return (e, 500)
