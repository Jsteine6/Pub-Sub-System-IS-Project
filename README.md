Manhattan Associates Pub/Sub Integration
IS 4880 | Capstone Consulting Project
📋 Project Overview
This project develops a scalable, decoupled messaging architecture using a Publisher/Subscriber (Pub/Sub) model. Our goal is to streamline data flow and real-time event processing for Manhattan Associates' logistics and supply chain environment.

🏗️ System Architecture & Team Roles
The project is structured into specialized technical pillars to ensure modularity:

Jack Steiner – Publisher Systems

Responsibility: Implementing Python-based logic to format and transmit data into the messaging stream.

Dan – Consumer/Subscriber Logic

Responsibility: Developing the subscriber scripts that pull messages from the topic for processing.

Dan – Operations & Systems Admin

Responsibility: Managing Git workflow, environment variables, and overall system orchestration.

Farid – Database Architecture (SQLite)

Responsibility: Managing the SQLite persistence layer to store and organize data received by the consumers.

Olivia – UI/UX Design

Responsibility: Creating a visual dashboard to monitor system activity and message history.

🛠️ Technical Stack
Language: Python 3.x

IDE: VS Code

Messaging: [e.g., Google Cloud Pub/Sub or PyPubSub]

Database: SQLite 3

Frontend/UI: Vibe / Python UI Framework

📂 Project Structure
Plaintext
├── publisher/
│   └── pub_client.py     # Jack's Workspace
├── subscriber/
│   └── sub_client.py     # Dan's Workspace
├── database/
│   └── data_store.db     # Farid's Workspace
├── ui/
│   └── dashboard.py      # Olivia's Workspace
└── README.md
