from google.cloud import pubsub_v1
import json
import uuid
import datetime
import time

project_id = "project-a423fd6a-a163-4972-bec"
topic_id = "alert-messaging-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

messages = [
    # --- Critical (5) ---
    ("critical", "Fire detected in Building A - Evacuate immediately"),
    ("critical", "Security breach on floor 3 - Lockdown initiated"),
    ("critical", "Gas leak reported in basement - All staff evacuate"),
    ("critical", "Active threat detected on campus - Shelter in place"),
    ("critical", "Server room flooding - Emergency shutdown required"),

    # --- High (5) ---
    ("high", "Power outage reported in Server Room B"),
    ("high", "Severe weather warning - Stay indoors"),
    ("high", "Network failure detected on primary router"),
    ("high", "Unauthorized access attempt on admin portal"),
    ("high", "Backup generator running at critically low fuel"),

    # --- Medium (5) ---
    ("medium", "HVAC system malfunction in Zone 2"),
    ("medium", "Scheduled maintenance overdue for elevator 4"),
    ("medium", "Water leak detected in basement storage"),
    ("medium", "Server CPU usage exceeding 85% threshold"),
    ("medium", "Employee badge system offline in Wing C"),

    # --- Low (5) ---
    ("low", "Routine inspection completed for fire extinguishers"),
    ("low", "Monthly safety drill scheduled for next Friday"),
    ("low", "Software update available for security terminals"),
    ("low", "Conference room B projector bulb needs replacing"),
    ("low", "Office supply restock requested by admin team"),
]

def publish_message(severity, content):
    payload = {
        "message_id": str(uuid.uuid4()),
        "content": content,
        "severity": severity,
        "created_at": str(datetime.datetime.now()),
    }

    raw = json.dumps(payload).encode("utf-8")
    future = publisher.publish(topic_path, raw)
    future.result()
    print(f"✅ [{severity.upper()}] {content}")
    time.sleep(0.3)

print("=== Sending 20 messages (5 per severity) ===\n")

for severity, content in messages:
    publish_message(severity, content)

print(f"\n=== All 20 messages sent ===")