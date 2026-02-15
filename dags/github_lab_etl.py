from airflow.decorators import dag, task
from datetime import datetime, timedelta
import requests
import pandas as pd
import sqlite3
import os

# Configuration
REPO_OWNER = 'Pranjal-Patil-Pers'
REPO_NAME = 'spectral_analysis'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
DB_PATH = '/opt/airflow/data/labpulse.db'

default_args = {
    'owner': 'LabPulse',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='labpulse_github_etl',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False
)
def github_etl():

    @task()
    def extract_commits():
        """Extract commits from the last 24 hours"""
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        since = (datetime.now() - timedelta(days=1)).isoformat()
        
        response = requests.get(url, headers=headers, params={'since': since})
        response.raise_for_status()
        return response.json()

    @task()
    def transform_commits(raw_commits):
        """Clean data and prepare for storage"""
        if not raw_commits:
            return []
            
        data = []
        for c in raw_commits:
            data.append({
                'sha': c['sha'],
                'author': c['commit']['author']['name'],
                'date': c['commit']['author']['date'],
                'message': c['commit']['message'],
                'url': c['html_url']
            })
        return data

    @task()
    def load_to_db(clean_data):
        """Load data into SQLite"""
        if not clean_data:
            print("No new commits to load.")
            return

        df = pd.DataFrame(clean_data)
        conn = sqlite3.connect(DB_PATH)
        df.to_sql('lab_activity', conn, if_exists='append', index=False)
        conn.close()
        print(f"Successfully loaded {len(df)} commits.")

    # Flow
    raw = extract_commits()
    clean = transform_commits(raw)
    load_to_db(clean)

# Instantiate
github_etl_dag = github_etl()
