import base64
from google.cloud import pubsub_v1
from visits import inc_visits


def create_topic(project_id: str, topic_id: str) -> None:
    """Create a new Pub/Sub topic."""
    # [START pubsub_quickstart_create_topic]
    # [START pubsub_create_topic]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    topic = publisher.create_topic(request={"name": topic_path})

    print(f"Created topic: {topic.name}")


def create_subscription(project_id: str, topic_id: str, subscription_id: str) -> None:
    """Create a new pull subscription on the given topic."""
    # [START pubsub_create_pull_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscription = subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )

    print(f"Subscription created: {subscription}")
    # [END pubsub_create_pull_subscription]


def consume(project_id: str, subscription_id: str):
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        try:
            inc_visits({"data": base64.b64encode(message.data)}, None)
            message.ack()
            print("consumed", message)
        except Exception as e:
            message.nack()
            print("not consumed", message, e)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    with subscriber:
        streaming_pull_future.result()


if __name__ == "__main__":
    try:
        create_topic("test", "visits")
    except Exception as e:
        print(e)
    try:
        create_subscription("test", "visits", "visits")
    except Exception as e:
        print(e)

    print("start consuming")
    consume("test", "visits")
