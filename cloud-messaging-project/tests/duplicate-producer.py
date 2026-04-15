from google.cloud import pubsub_v1
import json
import uuid
import datetime

project_id = "project-a423fd6a-a163-4972-bec"
topic_id = "alert-messaging-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def now():
    return str(datetime.datetime.now())

def publish_raw(payload: dict, label: str):
    raw = json.dumps(payload).encode("utf-8")
    future = publisher.publish(topic_path, raw)
    future.result()
    print(f"Published [{label}]: {payload}")

print("=== Duplicate Tests ===\n")

# Send the same message twice with the same message_id
duplicate_id = str(uuid.uuid4())
publish_raw({
    "message_id": duplicate_id,
    "content": "Duplicate test message",
    "severity": "high",
    "created_at": now()
}, "ORIGINAL")
 
publish_raw({
    "message_id": duplicate_id,
    "content": "Duplicate test message",
    "severity": "high",
    "created_at": now()
}, "DUPLICATE")
