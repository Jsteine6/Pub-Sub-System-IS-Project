from google.cloud import pubsub_v1
import json
import uuid
import datetime

# GCP variables
project_id = "project-a423fd6a-a163-4972-bec"
topic_id = "alert-messaging-topic"

# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Message publishing function
def publish_message(content, severity):
    message_id = str(uuid.uuid4()) 
    timestamp = datetime.datetime.now()
    created_at = str(timestamp)
    
    payload = {
        "message_id": message_id,
        "content": content,
        "severity": severity,
        "created_at": created_at,
    }

    #encrypt the payload
    message_json = json.dumps(payload)
    message_bytes = message_json.encode("utf-8")

    #publish message to topic 
    #and store the result
    future = publisher.publish(topic_path, message_bytes)
    published_id = future.result()

    print(f"\nMessage published (Message Payload: {payload})\n")
    return message_id

if __name__ == "__main__":
    print("=== Producer Started ===")

    while True:
        user_input = input("Enter message (or type 'exit'): ")

        if user_input.lower() == "exit":
            print("Exiting producer...")
            break

        publish_message(user_input)