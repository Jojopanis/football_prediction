from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import os
import sys
sys.path.insert(0, '/opt/airflow')

from utils.soup import download_csv

args = {
    'owner': 'AlperC',
    'start_date': days_ago(1)  # makes start date in the past
}

dag = DAG(
    dag_id='weekly_scraper_dag',
    default_args=args,
    schedule_interval='1 0 * * 1'  # runs every Monday at 00:01
)

with dag:
    task = PythonOperator(
        task_id='weeklystats',
        python_callable=download_csv
    )

task