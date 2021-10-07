from os import environ
from google.cloud import pubsub_v1

PUBLISHER = pubsub_v1.PublisherClient()
TOPIC_PATH = PUBLISHER.topic_path(
    environ.get("PROJECT_ID", "taller3-pcuneo"), environ.get("TOPIC_ID", "visits")
)


def post_visits(page_name):
    message_bytes = page_name.encode("utf-8")
    try:
        publish_future = PUBLISHER.publish(TOPIC_PATH, data=message_bytes)
        publish_future.result()
        return "Ok"
    except Exception as e:
        print(e)
        return (e, 500)
