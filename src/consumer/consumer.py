from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import json
import sqlite3

#GCP variables
project_id = "project-a423fd6a-a163-4972-bec"
subscription_id = "alert-messaging-topic-sub"
timeout = 30.0 # Number of seconds the subscriber should listen for messages

# sqlite3 Setup - creates DB file
con = sqlite3.connect('messaging-database', check_same_thread=False)
cursor = con.cursor() # cursor object to execute sql commands

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL,
    content TEXT NOT NULL,
    severity TEXT,
    created_at TEXT NOT NULL,
    is_duplicate BOOLEAN
)
''')
con.commit()

# Establish connection to pubsub subscription
# 'subscriber_path' creates a path that looks like this: projects/{project_id}/topics/{topic_id}
subscriber = pubsub_v1.SubscriberClient()
subscriber_path = subscriber.subscription_path(project_id, subscription_id)

# Check payload for missing fields and data value accuracy
def validate_payload(payload: dict):
    required_fields = ["message_id", "content", "severity", "created_at"]

    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(payload["message_id"], str):
        raise ValueError("message_id must be a string")

    if not isinstance(payload["content"], str):
        raise ValueError("content must be a string")

    if not isinstance(payload["severity"], str):
        raise ValueError("severity must be a string")

    if not isinstance(payload["created_at"], str):
        raise ValueError("created_at must be a string")

# Check the database for duplicates using 'message_id'
def check_duplicate(message_id: str) -> bool:
    cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM messages WHERE message_id = ?)",
        (message_id,)
    )
    return bool(cursor.fetchone()[0])

# Insert message into DB
def insert_message(payload: dict, is_duplicate: bool):
    cursor.execute("""
        INSERT INTO messages (message_id, content, severity, created_at, is_duplicate)
        VALUES (?, ?, ?, ?, ?)
    """, (
        payload["message_id"],
        payload["content"],
        payload["severity"],
        payload["created_at"],
        is_duplicate
    ))
    con.commit()

# Receive message from pubsub subscription
def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    try:
        # Decode and parse message
        decoded = message.data.decode("utf-8")
        payload = json.loads(decoded)
        print("Received payload:", payload)

        # Validate payload structure
        validate_payload(payload)
        message_id = payload["message_id"]

        # Check for duplicates
        is_duplicate = check_duplicate(message_id)

        # Insert message to DB with duplicate flag
        insert_message(payload, is_duplicate)
        print("Message added to database:", payload, "is_duplicate:", is_duplicate)

        # Ack message
        message.ack()

    except Exception as e:
        print("Error processing message:", e)
        # Ack invalid messages to prevent infinite loop
        message.ack()

streaming_pull_future = subscriber.subscribe(subscriber_path, callback=callback)
print(f"Listening for messages on {subscriber_path}\n")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    streaming_pull_future.result()