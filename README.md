# LabPulse: Automated GitHub ETL Pipeline

**LabPulse** is a data engineering project designed to monitor research activity and code contributions in a laboratory environment. Built with **Apache Airflow**, it automates the extraction of commit metadata from the GitHub REST API, transforms the data into a clean format, and loads it into a structured database for long-term tracking.

[Image of GitHub ETL pipeline architecture using Airflow and SQLite]

---

## 🚀 Features
* **Automated Extraction**: Scheduled daily pulls from the GitHub REST API using Python's `requests`.
* **Data Transformation**: Cleans raw JSON responses and flattens nested commit data into a structured schema using `Pandas`.
* **Local Data Warehouse**: Persists data into a local **SQLite** database, enabling easy analysis of lab productivity.
* **Containerized Orchestration**: Managed entirely via **Docker Compose** to ensure a reproducible environment for all lab members.

---

## 🛠️ Tech Stack
* **Orchestration**: Apache Airflow 2.x
* **Language**: Python 3.8+
* **Data Libraries**: Pandas, Requests
* **Database**: SQLite
* **Infrastructure**: Docker, Docker Compose
* **IDE**: VS Code

---

## 📁 Project Structure
```text
labpulse/
├── dags/
│   └── github_lab_etl.py     # Main ETL logic (Extract, Transform, Load)
├── data/
│   └── labpulse.db           # SQLite database file (Persistent storage)
├── docker-compose.yaml      # Multi-container Airflow setup
├── Dockerfile               # Custom Airflow image with dependencies
├── .env                     # Secrets (GitHub Token, Airflow UID)
└── requirements.txt         # Python dependencies (pandas, requests)
---
## ⚙️ Setup & Installation
***1. Prerequisites**
Docker Desktop installed and running.

GitHub Personal Access Token (PAT) with repo scopes.

***2. Environment Configuration**
Create a .env file in the root directory:
@bash
AIRFLOW_UID=50000
GITHUB_TOKEN=ghp_your_secret_token_here

***3. Deployment**
Run the following commands in your VS Code terminal:
@bash
# Set folder permissions (Crucial for SQLite write access on Mac/Linux)
chmod -R 777 ./data

# Initialize the Airflow metadata database
docker compose up airflow-init

# Start the pipeline
docker compose up -d

Access the Airflow UI at http://localhost:8080 (Default: airflow / airflow).
---
## 📊 Sample Data Insights
Once the pipeline is triggered, you can query labpulse.db to view:

Total Commits: Frequency of code updates to specific lab repos.

Contributor Heatmap: Identifying which researchers are most active.

Commit Velocity: Tracking if the pace of a research project (like spectral_analysis) is increasing.
---
##🛡️ Challenges Overcome
API Security: Implemented secure environment variable mapping from Docker to Airflow to protect GitHub credentials.

Container Permissions: Resolved sqlite3.OperationalError by managing volume write-permissions between the host Mac and the Docker container.

Task Retries: Configured Airflow's retry logic to handle temporary network timeouts and GitHub rate-limiting gracefully.
---
## 🔮 Future Enhancements
[ ] Slack Integration: Send a weekly summary of lab commits to a Slack channel.

[ ] Grafana Dashboard: Connect the SQLite database to a visual dashboard.

[ ] Cloud Migration: Move the database to AWS RDS or Google BigQuery.
