from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from ..csv_scraper import release_the_spider

args = {
    'owner' : 'AlperC',
    'start_date': days_ago(1) #makes start date in the past
}

dag = DAG(
    dag_id = 'weekly_scraper_dag',
    default_args = args,
    schedule_interval = '1 0 * * 1' #runs on every week monday at 00:01
)

with dag:
    task = PythonOperator(
        task_id = 'weeklystats',
        python_callable = release_the_spider,
        provide_context = True
    )

task